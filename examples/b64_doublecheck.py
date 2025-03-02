from trl import GRPOTrainer
import verifiers as vf
from verifiers.prompts import B64_PROMPT, B64_FEW_SHOT
from peft import LoraConfig

model_name = "Qwen/Qwen2.5-14B-Instruct"
model, tokenizer = vf.get_model_and_tokenizer(model_name)

vf_env = vf.B64Env(dataset="b64-single", system_prompt=B64_PROMPT, few_shot=B64_FEW_SHOT[0])
dataset = vf_env.get_dataset()
rubric = vf_env.get_rubric()
training_args = vf.get_default_grpo_config(run_name="b64-single-qwen2.5-14b-attempt-3-mlp-lora", num_gpus=8)
lora_rank = 64
lora_config = LoraConfig(
    r=lora_rank,
    target_modules=["up_proj", "down_proj", "gate_proj"],
    modules_to_save=[
        "lm_head",
        "embed_tokens",
        "norm",
        "input_layernorm",
        "post_attention_layernorm",
        "rotary_emb",
        "q_proj",
        "v_proj",
        "k_proj",
        "o_proj",
    ],
    lora_alpha=lora_rank,
    lora_dropout=0.1,
)
trainer = GRPOTrainer(
    model=model,
    processing_class=tokenizer,
    reward_funcs=rubric, 
    env=vf_env,
    args=training_args,
    train_dataset=dataset,
    peft_config=lora_config,
)
trainer.train()