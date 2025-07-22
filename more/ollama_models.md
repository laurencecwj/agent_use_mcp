# 使用ollama

qwen3:32b可以完全正确，它会自动修正并重新提交，解决所有调用tools过程里面出现的异常，包括os包不允许使用这类pandas-mcp给出的出错限制。但是太慢，在L4上差不多要20来分钟。

qwen3:14b运行结果不正确。有代码但没去执行。

qwen3:8b-q8_0同样文件正确，甚至写了代码也没去执行。

qwen2.5-coder:7b没有执行代码。

qwen2.5-coder:14b没有执行代码。

llama3.1:8b乱七八糟。

以下都用的第三方的api，非ollama。

moonshotai/Kimi-K2-Instruct:工具没用好，不会提交代码。

deepseek-ai/DeepSeek-V3-0324:一共2个excel，其中带smiles这列的处理完美，另一个没有to lower case，所以没有拿到结果。

Qwen/Qwen3-30B-A3B:光说不练，没有往mcp做完美的提交。

Qwen/Qwen3-235B-A22B:最后处理function calling内部有问题。也就是生成的内容不符合规范。

THUDM/GLM-4-32B-0414:任务都没完成，乱提交。

Qwen/Qwen2.5-72B-Instruct:提交都不正常。

deepseek-ai/DeepSeek-R1:看起来以假乱真，感觉对了；但实际上chembl.xlsx的mean不对，应用该是63.76939203354298，但它居然是49.2不知道怎么来的。

Qwen/Qwen3-32B:在线siliconflow有问题。

qwen-coder-plus:chembl.xlsx里面的sheet它没找到，另一个对的。

qwen-turbo-2025-02-11:没有提交代码计算长度。

qwen-plus-2025-01-25:正确，完美。

qwen-max:正确，完美。

qwq-plus:处理出错，应该跟function calling有关。

#### 1. 配置修改

修改mcp_agent.config.yaml 

```yaml
openai:
    base_url: "http://localhost:11434/v1"
    api_key: ollama
    default_model: qwen3:32b
```

另外可以直接删掉mcp_agent.secrets.yaml，以防它自动使用了其中的配置

#### 2. 代码修改

```python
# 把demo.py中这行最开始的注释去掉，使用它
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

# 后续中 llm = await finder_agent.attach_llm(GoogleAugmentedLLM)
# 改成
llm = await finder_agent.attach_llm(OpenAIAugmentedLLM)

```

#### 3. 运行结果

其它的运行方法不变

结果在result_ollama_qwen3_32b.tar.gz