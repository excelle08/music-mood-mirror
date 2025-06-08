# Feedbacks to AI Studio

## Coding with AI Studio Workspace

When I used the Jupyter notebook in the AI studio do conduct some analysis works on the music listening history,
I stored the notebook directly under the home folder without knowing that all files and data outside the
`local` and `shared` folders would be lost upon restart. Therefore I lost the notebook and had to rewrite
the code for analysis one week later when the computer rebooted.

**Feedback**: The default behavior of the AI studio workspace container when the user closes the AIS
or the system crashes should be to "pause" and
preserve the states. A full stop and state cleanup should be only done if the user explicitly requests so,
for example, through a "stop" button and there should be warnings given prior to doing the state wipeout.

## Model Deployment

### Model Registrations to MLFlow

When registering the LLM model we intended to use to MLFlow, we initially followed the
[example](https://zdocs.datascience.hp.com/docs/aistudio/using-aistudio/model-deployment/register-model-mistral)
provided in AI Studio's documentations. However, it did not work: after we registered the model to MLFlow using
the example code and deployed the model as a service in AIS, the API created by Swagger UI always returned
`{"predictions": null}`.

After extensive debugging and consultation with the LLM agent, we learned that we needed to also implement
a `predict` method in the `AIStudioChatbotService` in order for the deployed model to work.

**Feedback**: The [documentation](https://zdocs.datascience.hp.com/docs/aistudio/using-aistudio/model-deployment/register-model-mistral#register-the-model)
should have mentioned that we needed to initialize the model in the constructor or `load_context` method _and_
implement a `predict` method to perform the actual model inference with input data. It would be better if the
sample code could provide a minimal working example of the model initialization and the `predict` method, and
provide guidance on what dependencies of which versions (that are compatible with the AIS workspace) to install.

### Model Deployment with AI Studio

After implementing the model initialization and the `predict` method, we had a very hard time and were not successful in
using AI Studio to deploy the registered model as a service. When we attempted to start the deployment, it spent very
long time before it failed with the following message:

```
Top Failure Reasons
* Make sure you have selected the correct model and version
* Make sure you have selected the correct workspace to run the model service in
* Make sure custom libraries don't conflict with libraries present in the base image
* Make sure you haven't installed a custom version of MLFlow as a custom library
```

This message is not very helpful for us to understand why the deployment failed, and it did not point us to any actual
log for debugging. Therefore, we had to give up deploying the model with AIS and pivot to loading the model with the
web app. We tested in the AIS workspace that the registered model did work using the following code:

```python
loaded_model = mlflow.pyfunc.load_model(model_uri) 
m_input={'prompt':"What is MLflow?", "query": "", "document": ""}
res = loaded_model.predict(m_input)
print(res)
```

**Feedback**: AIS should have provided a log when the local model deployment fails to help us debug what the issue is,
instead of just slapping us with a very general message.

### Model Executions

We initially intended to use the model downloaded from the Model Catalog (e.g. Gemma 2B Instruct TensorRT LLM), but
it took us quite long time to figure out that this model needs to be executed by the `tensorrt_llm` framework.
As we were trying the `tensorrt_llm` framework, we've been facing a series of errors:

#### Dependency problems

- Unable to find libpython3.12: `ImportError: libpython3.12.so.1.0: cannot open shared object file: No such file or directory `
- One of the dependencies of `tensorrt_llm`, `flashinfer-python 0.2.6` failed to build. Had to explicitly install
  `flashinfer-python==0.2.3` first to install `tensorrt_llm`
- We were able to install `tensorrt_llm` but pip gave a lot of errors of dependent packages conflicting with
  other existing ones

#### Model Compatibility problems

- The model artifact's `config.json` seemed to be not compatible with the current version of `tensorrt_llm`. For example,
  it kept raising errors like missing keys `max_seq_len`, `kv_cache_type`, etc.

**Feedback**: It would be more helpful to provide some guide and perhaps a snippet of sample code on what is the right
framework and how to execute the models obtained in the Model Catalog.

### Problems with the containers / workspace images

We've been encountering different problems on the containers we tried:

#### Deep Learning GPU

When we wanted to install model execution frameworks, such `llama-cpp-python`, `transformers` and
`tensorrt_llm`, we've been seeing lots of dependency errors, most of which are related to the versions of
packages being installed is conflicting to 

**Feedback**: We hope the AI Studio's documentation can provide some recommendations on what version of these commonly
used AI packages we should install so that they can be compatible with the packages and libraries preloaded
on the workspace container.

#### Nemo Framework

This container does not allow Git extension in its jupyter lab environment. This is a constraint we
do not understand and is very inconvenient for our collaboration.

#### TensorRT-LLM Release

Although this container image is advertised to provide the TensorRT-LLM package, it does not really work.
When I tried `import tensorrt_llm` in the jupyter console of this container with the `aistudio` kernel,
it would give an error `ImportError: libnvinfer.so.10: cannot open shared object file: No such file or directory`.

Besides, this container does not seem to give root access, it would require password when we attempted to `sudo`.

**Feedback**: We hope in the future these types of containers can be made really self contained and users can import
`tensorrt_llm` without any problems and worries about installing other dependencies.

## AI-Blueprint Examples

We tried looking at the sample projects in the [AI-Blueprints](https://github.com/HPInc/AI-Blueprints) Github repo
to learn more about how to develop the project. However, the sample projects were not very helpful for us especially
in terms of understanding how to choose the right type of workspace and how to install appropriate dependencies.

For example, several Gen-AI related projects, such as
[Automated Evaluation with Structured Outputs](https://github.com/HPInc/AI-Blueprints/tree/main/generative-ai/automated_evaluation_with_structured_outputs) and
[Text Generation with Galileo](https://github.com/HPInc/AI-Blueprints/tree/main/generative-ai/galileo/03-text-generation-with-langchain)
mentioned to choose "**Local GenAI**" as the base image when creating the workspace, but "Local GenAI" does not exist
in the image catalog when we were trying to create a workspace.

Also, in the example of [Agentic RAG for AI Studio with TRT-LLM and LangGraph](https://github.com/HPInc/AI-Blueprints/tree/main/generative-ai/agentic_rag_with_trt-llm_and_langgraph),
the project used `tensorrt_llm` package, but it did not provide any instruction on how to properly install this
package. `tensorrt_llm` was also not provided in the NeMo framework workspace out-of-box.

**Feedback**: It would be nicer for participants if the sample projects have more helpful guides on choosing the
right workspace image for their work and installing the right depdendency packages with proper, non-conflicting versions.

## Reliability

There's some room of improvement in AI Studio's reliability as it sometimes has bugs. For example, I once
encountered a problem that the AI studio would freeze if I typed anything in the terminal of the workspace.
The problem resolved on its own after I rebooted the computer.