from typing import List, Dict, Any

from datasets import Dataset
from trl.trainer.grpo_trainer import RewardFunc

from verifiers.envs.multistep_env import MultiStepEnv
from verifiers.prompts import SIMPLE_PROMPT, DOUBLECHECK_FEW_SHOT
from verifiers.rubrics import MathRubric
from verifiers.utils import preprocess_dataset
import base64


class B64Env(MultiStepEnv):
    def __init__(self, 
                 dataset: str = "b64-single",
                 system_prompt: str = SIMPLE_PROMPT,
                 few_shot: List[Dict[str, str]] = DOUBLECHECK_FEW_SHOT[0],
                 max_steps: int = 5,
                 **kwargs):
        
        sampling_args = {
            "skip_special_tokens": False,
            "spaces_between_special_tokens": False,
        }
        super().__init__(dataset=dataset, system_prompt=system_prompt, few_shot=few_shot, sampling_args=sampling_args, **kwargs)
        self.dataset_name = dataset
        self.dataset = preprocess_dataset(
            dataset_name=dataset,
            split="train",
            system_prompt=system_prompt,
            few_shot=few_shot
        )
        self.rubric = MathRubric()
        self.max_steps = max_steps

    def get_rubric(self, **kwargs: Any) -> List[RewardFunc]:
        return self.rubric.get_reward_funcs()
    
    def get_dataset(self, **kwargs: Any) -> Dataset:
        return self.dataset
    
    def is_completed(self, messages: List[Dict[str, str]], **kwargs: Any) -> bool:
        def is_correct():
            # for efficiency, and it should also be at the end of the message
            return base64.b64decode(messages[-2]['content']).decode('utf-8') in messages[-1]['content'][-100:]
        return len(messages) >= self.max_steps or is_correct()
    
    def env_response(self, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, str]:
        return {'role': 'user', 'content': 'Unfortunatly, the decoding is incorrect. Verify the decoding and return the correct answer.'}