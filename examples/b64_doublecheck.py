from trl import GRPOTrainer
import verifiers as vf
from verifiers.prompts import B64_PROMPT, B64_FEW_SHOT

model_name = "Qwen/Qwen2.5-14B-Instruct"
model, tokenizer = vf.get_model_and_tokenizer(model_name)

vf_env = vf.DoubleCheckEnv(dataset="b64-single", system_prompt=B64_PROMPT, few_shot=B64_FEW_SHOT[0])
dataset = vf_env.get_dataset()
rubric = vf_env.get_rubric()
training_args = vf.get_default_grpo_config(run_name="b64-single-qwen2.5-14b-attempt-2", num_gpus=8)
trainer = GRPOTrainer(
    model=model,
    processing_class=tokenizer,
    reward_funcs=rubric, 
    env=vf_env,
    args=training_args,
    train_dataset=dataset,
)
trainer.train()