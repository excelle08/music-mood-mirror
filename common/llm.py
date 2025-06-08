import os
import mlflow
from mlflow.pyfunc import PythonModel
from mlflow.models.signature import ModelSignature
from mlflow.types.schema import Schema, ColSpec, ParamSchema, ParamSpec
from llama_cpp import Llama


HOME = os.environ.get("HOME")
loaded_model = None


class MusicMoodMirrorAIService(PythonModel):
    def __init__(self):
        super().__init__()
        self.model_path = f"{HOME}/models/gemma-2b-it.Q4_K_M.gguf"
        self._llama = Llama(
            model_path=self.model_path,
            n_gpu_layers=35,
            n_ctx=8192,
            verbose=False
        )

    def predict(self, context, model_input):
        prompt = model_input["prompt"][0]
        print(f"Type of prompt is: {type(prompt)}")
        # output = self.llama(prompt)
        result = self._llama(prompt, temperature=0.0, max_tokens=256, stop=["</s>"])
        text = result["choices"][0]["text"]
        outputs={
                "chunks": "",
                "history": "",
                "prompt": prompt,
                "output": text.strip(),
                "success": True
        }
        return outputs

    @classmethod
    def log_model(cls, model_folder=None, demo_folder="demo"):
        # Ensure the demo folder exists
        if demo_folder and not os.path.exists(demo_folder):
            os.makedirs(demo_folder, exist_ok=True)

        # Define input schema for the model
        input_schema = Schema([
            ColSpec("string", "query"),
            ColSpec("string", "prompt"),
            ColSpec("string", "document")
        ])

        # Define output schema for the model
        output_schema = Schema([
            ColSpec("string", "chunks"),
            ColSpec("string", "history"),
            ColSpec("string", "prompt"),
            ColSpec("string", "output"),
            ColSpec("boolean", "success")
        ])

        # Define parameters schema for additional settings
        param_schema = ParamSchema([
            ParamSpec("add_pdf", "boolean", False),
            ParamSpec("get_prompt", "boolean", False),
            ParamSpec("set_prompt", "boolean", False),
            ParamSpec("reset_history", "boolean", False)
        ])

        # Combine schemas into a model signature
        signature = ModelSignature(inputs=input_schema, outputs=output_schema, params=param_schema)

        # Define model artifacts
        artifacts = {"demo": demo_folder}
        if model_folder:
            artifacts["models"] = model_folder

        # Log the model in MLflow
        mlflow.pyfunc.log_model(
            artifact_path="music_mood_mirror_ai_service",
            python_model=cls(),
            artifacts=artifacts,
            signature=signature,
            pip_requirements=[
                "pyyaml",
                "tokenizers==0.20.3",
                "httpx==0.27.2",
            ]
        )
        print("Model and artifacts successfully registered in MLflow.")


def init_llm_model():
    # Initialize the MLflow experiment
    print("Initializing experiment in MLflow.")
    mlflow.set_experiment("MusicMoodMirrorAI_Service")

    # Define required paths
    model_folder = f"{HOME}/models/gemma-2b-it.Q4_K_M.gguf"
    demo_folder = "demo"

    # Ensure required directories exist before proceeding
    if demo_folder and not os.path.exists(demo_folder):
        os.makedirs(demo_folder, exist_ok=True)

    # Start an MLflow run and log the model
    with mlflow.start_run(run_name="Gemma_Test_Run_gguf_0607") as run:
        MusicMoodMirrorAIService.log_model(
            demo_folder=demo_folder,
            model_folder=model_folder
        )

        # Register the model in MLflow
        model_uri = f"runs:/{run.info.run_id}/music_mood_mirror_ai_service"
        mlflow.register_model(
            model_uri=model_uri,
            name="Gemma_test_0607",
        )
        print(f"Registered model with execution ID: {run.info.run_id}")
        print(f"Model registered successfully. Run ID: {run.info.run_id}")
    
    return model_uri


def load_llm_model(model_uri: str):
    print(f"Loading model from URI: {model_uri}")
    global loaded_model
    loaded_model = mlflow.pyfunc.load_model(model_uri)
    print("Testing the loaded model with a sample input...")
    m_input={'prompt':"What is MLflow?", "query": "", "document": ""}
    res = loaded_model.predict(m_input)
    print(f"Model loaded successfully. Sample output: {res['output']}")


if __name__ == "__main__":
    try:
        model_uri = init_llm_model()
        load_llm_model(model_uri)
    except Exception as e:
        print(f"Error initializing or loading LLM model: {e}")