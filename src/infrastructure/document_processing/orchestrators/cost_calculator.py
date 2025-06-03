# src/infrastructure/document_processing/orchestrators/cost_calculator.py

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

from src.core.models.document import Document, DocumentChunk
from src.core.utils.logger import Logger

logger = Logger(__name__)


@dataclass
class ModelPricing:
    """Pricing information for AI models."""
    provider: str
    model: str
    input_cost_per_1k: float  # USD per 1K input tokens
    output_cost_per_1k: float  # USD per 1K output tokens
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate total cost for given token usage."""
        input_cost = (input_tokens / 1000) * self.input_cost_per_1k
        output_cost = (output_tokens / 1000) * self.output_cost_per_1k
        return input_cost + output_cost


class CostCalculator:
    """Calculate and track costs for document processing."""
    
    def __init__(self):
        self.pricing = self._initialize_pricing()
        self.usage_history = []
        
    def _initialize_pricing(self) -> Dict[str, ModelPricing]:
        """Initialize current model pricing (as of June 2025)."""
        return {
            # OpenAI Models
            "gpt-3.5-turbo": ModelPricing(
                provider="openai",
                model="gpt-3.5-turbo",
                input_cost_per_1k=0.0005,
                output_cost_per_1k=0.0015
            ),
            "gpt-4-turbo-preview": ModelPricing(
                provider="openai", 
                model="gpt-4-turbo-preview",
                input_cost_per_1k=0.01,
                output_cost_per_1k=0.03
            ),
            "gpt-4o": ModelPricing(
                provider="openai",
                model="gpt-4o",
                input_cost_per_1k=0.005,
                output_cost_per_1k=0.015
            ),
            
            # Anthropic Models
            "claude-3-sonnet-20240229": ModelPricing(
                provider="anthropic",
                model="claude-3-sonnet",
                input_cost_per_1k=0.003,
                output_cost_per_1k=0.015
            ),
            "claude-3-opus-20240229": ModelPricing(
                provider="anthropic",
                model="claude-3-opus",
                input_cost_per_1k=0.015,
                output_cost_per_1k=0.075
            ),
            "claude-3-haiku-20240307": ModelPricing(
                provider="anthropic",
                model="claude-3-haiku",
                input_cost_per_1k=0.00025,
                output_cost_per_1k=0.00125
            ),
            
            # Google Models
            "gemini-1.5-flash": ModelPricing(
                provider="google",
                model="gemini-1.5-flash",
                input_cost_per_1k=0.00035,
                output_cost_per_1k=0.00105
            ),
            "gemini-1.5-pro": ModelPricing(
                provider="google",
                model="gemini-1.5-pro",
                input_cost_per_1k=0.00125,
                output_cost_per_1k=0.00375
            )
        }
    
    def estimate_document_cost(
        self,
        document: Document,
        output_format: str,
        model_strategy: Dict[str, str]
    ) -> Dict[str, float]:
        """
        Estimate processing cost for entire document.
        
        Args:
            document: Document to process
            output_format: Target format (podcast, course, etc.)
            model_strategy: Mapping of task types to models
            
        Returns:
            Cost breakdown by model and total
        """
        # Estimate tokens
        total_input_tokens = document.estimate_tokens()
        
        # Output multipliers based on format
        output_multipliers = {
            "translation": 1.0,
            "summary": 0.2,
            "podcast": 1.5,
            "course": 2.0,
            "video": 0.8,
            "screenplay": 1.2
        }
        
        output_multiplier = output_multipliers.get(output_format, 1.0)
        estimated_output_tokens = int(total_input_tokens * output_multiplier)
        
        # Calculate costs per model
        cost_breakdown = {}
        total_cost = 0.0
        
        for task_type, model_name in model_strategy.items():
            if model_name in self.pricing:
                pricing = self.pricing[model_name]
                
                # Estimate portion of document for this task
                task_portion = self._estimate_task_portion(task_type)
                task_input_tokens = int(total_input_tokens * task_portion)
                task_output_tokens = int(estimated_output_tokens * task_portion)
                
                cost = pricing.calculate_cost(task_input_tokens, task_output_tokens)
                cost_breakdown[f"{task_type}_{model_name}"] = cost
                total_cost += cost
        
        cost_breakdown["total"] = total_cost
        
        # Add breakdown by provider
        provider_costs = {}
        for model_name, pricing in self.pricing.items():
            provider = pricing.provider
            if provider not in provider_costs:
                provider_costs[provider] = 0.0
                
        for key, cost in cost_breakdown.items():
            if key != "total":
                model_name = key.split("_", 1)[1]
                if model_name in self.pricing:
                    provider = self.pricing[model_name].provider
                    provider_costs[provider] += cost
                    
        cost_breakdown["by_provider"] = provider_costs
        
        return cost_breakdown
    
    def _estimate_task_portion(self, task_type: str) -> float:
        """Estimate what portion of document processing a task represents."""
        task_portions = {
            "outline": 0.05,
            "summary": 0.10,
            "main_processing": 0.70,
            "refinement": 0.10,
            "formatting": 0.05
        }
        return task_portions.get(task_type, 0.2)
    
    def calculate_chunk_cost(
        self,
        chunk: DocumentChunk,
        model_name: str,
        estimated_output_tokens: Optional[int] = None
    ) -> float:
        """Calculate cost for processing a single chunk."""
        if model_name not in self.pricing:
            logger.warning(f"Unknown model: {model_name}")
            return 0.0
            
        pricing = self.pricing[model_name]
        
        # Estimate tokens
        input_tokens = int(chunk.word_count * 1.33)
        
        if estimated_output_tokens is None:
            # Default estimate based on chunk type
            chunk_type = chunk.metadata.get("type", "general")
            output_ratios = {
                "summary": 0.2,
                "scene": 1.5,
                "dialogue": 1.2,
                "general": 1.0
            }
            ratio = output_ratios.get(chunk_type, 1.0)
            estimated_output_tokens = int(input_tokens * ratio)
            
        return pricing.calculate_cost(input_tokens, estimated_output_tokens)
    
    def track_usage(
        self,
        model_name: str,
        input_tokens: int,
        output_tokens: int,
        cost: float,
        document_id: str,
        chunk_id: Optional[str] = None
    ):
        """Track model usage for analytics."""
        usage_record = {
            "timestamp": datetime.now(),
            "model": model_name,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost": cost,
            "document_id": document_id,
            "chunk_id": chunk_id
        }
        self.usage_history.append(usage_record)
        
    def get_usage_summary(self, time_period_hours: int = 24) -> Dict[str, any]:
        """Get usage summary for specified time period."""
        cutoff_time = datetime.now().timestamp() - (time_period_hours * 3600)
        recent_usage = [
            u for u in self.usage_history 
            if u["timestamp"].timestamp() > cutoff_time
        ]
        
        if not recent_usage:
            return {
                "total_cost": 0.0,
                "total_tokens": 0,
                "model_breakdown": {},
                "document_count": 0
            }
        
        # Calculate totals
        total_cost = sum(u["cost"] for u in recent_usage)
        total_tokens = sum(u["total_tokens"] for u in recent_usage)
        
        # Model breakdown
        model_breakdown = {}
        for usage in recent_usage:
            model = usage["model"]
            if model not in model_breakdown:
                model_breakdown[model] = {
                    "count": 0,
                    "cost": 0.0,
                    "tokens": 0
                }
            model_breakdown[model]["count"] += 1
            model_breakdown[model]["cost"] += usage["cost"]
            model_breakdown[model]["tokens"] += usage["total_tokens"]
        
        # Document count
        unique_documents = len(set(u["document_id"] for u in recent_usage))
        
        return {
            "total_cost": round(total_cost, 4),
            "total_tokens": total_tokens,
            "model_breakdown": model_breakdown,
            "document_count": unique_documents,
            "usage_count": len(recent_usage),
            "average_cost_per_use": round(total_cost / len(recent_usage), 4) if recent_usage else 0
        }
    
    def optimize_model_selection(
        self,
        required_quality: int,
        budget_per_1k_tokens: float,
        capabilities_needed: List[str]
    ) -> Optional[str]:
        """
        Select optimal model based on constraints.
        
        Args:
            required_quality: Minimum quality rating (1-10)
            budget_per_1k_tokens: Maximum cost per 1K tokens
            capabilities_needed: List of required capabilities
            
        Returns:
            Optimal model name or None if no match
        """
        from src.infrastructure.document_processing.orchestrators.model_orchestrator import ModelCapability
        
        candidates = []
        
        # Filter by budget
        for model_name, pricing in self.pricing.items():
            avg_cost = (pricing.input_cost_per_1k + pricing.output_cost_per_1k) / 2
            if avg_cost <= budget_per_1k_tokens:
                candidates.append(model_name)
        
        if not candidates:
            return None
            
        # Sort by cost-effectiveness
        candidates.sort(key=lambda m: (
            self.pricing[m].input_cost_per_1k + self.pricing[m].output_cost_per_1k
        ))
        
        return candidates[0] if candidates else None
