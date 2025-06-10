# Tracing Example with NeMo Guardrails

This example demonstrates how to set up tracing for NeMo Guardrails using OpenTelemetry and Zipkin, and how to configure content-safety rails using either OpenAI, NVIDIA, or a local Llama-Guard 3 model via Ollama.

## Directory Structure

```
src/examples/tracing/
├── config/         # Configuration files (YAML, rails, prompts)
│   ├── config.yml
│   ├── prompts.yml
│   └── rails/
│       └── rails_01.co
└── demo.py         # Example script for running Guardrails with tracing
```

---

## 1. Prerequisites

- Python 3.8+
- [Docker](https://www.docker.com/) (for Zipkin)
- [Ollama](https://ollama.com/) (optional, for local Llama-Guard 3)
- OpenAI or NVIDIA API keys (if using their hosted models)

---

## 1.1. Installing Tracing Dependencies with uv

This example uses the [`opentelemetry-exporter-zipkin`](https://pypi.org/project/opentelemetry-exporter-zipkin/) package for tracing, managed as an optional dependency group called `tracing` in the project.

To install the tracing dependencies using [uv](https://github.com/astral-sh/uv):

```sh
uv sync --group tracing
```

or 

```sh
uv sync --all-groups
```

- This will install all packages required for tracing, including the Zipkin exporter.
- Make sure you have [uv installed](https://github.com/astral-sh/uv#installation).

If you prefer, you can also install all dependencies (including tracing) with:

```sh
uv pip install .
```

Or just the main dependencies (without tracing):

```sh
uv pip install --group default .
```

---

## 2. Setting Up Zipkin for Tracing

Zipkin is used to collect and visualize traces from NeMo Guardrails via OpenTelemetry.

**Start Zipkin locally using Docker:**

```sh
docker run -d -p 9411:9411 openzipkin/zipkin
```

- Zipkin UI will be available at [http://localhost:9411](http://localhost:9411)
- Ensure your `config/config.yml` is set up to export traces to Zipkin (see [OpenTelemetry docs](https://opentelemetry.io/docs/instrumentation/python/exporters/)).

---

## 3. Setting API Keys in `.env`

Create a `.env` file in your project root (or ensure it exists) with the following variables:

```env
# For OpenAI
OPENAI_API_KEY=sk-...

# For NVIDIA NeMo Guardrails (if using NVIDIA/llama-3.1-nemoguard-8b-content-safety)
NVIDIA_API_KEY=nv-...

# (Optional) For local Ollama, see below
```

- The `demo.py` script loads these variables using `python-dotenv`.
- If you use Ollama for local Llama-Guard, set the variables as described in section 5.

---

## 4. Using OpenAI or NVIDIA Content-Safety Models

- By default, the example expects an `OPENAI_API_KEY` in your environment.
- If using NVIDIA's content-safety model (`nvidia/llama-3.1-nemoguard-8b-content-safety`), set `NVIDIA_API_KEY` as well.

---

## 5. Using Local Llama-Guard 3 with Ollama

You can run Meta’s Llama-Guard 3 locally for content-safety using [Ollama](https://ollama.com/).

### Step 1: Install and Run Ollama

**macOS (Homebrew):**
```sh
brew install ollama
ollama serve
```

**Ubuntu/Debian:**
```sh
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

- Ollama runs a REST server at `http://localhost:11434`.

### Step 2: Pull Llama-Guard 3 Model

```sh
# 1B parameter model (fast, low-RAM)
ollama pull llama-guard3:1b

# 8B parameter model (recommended)
ollama pull llama-guard3:8b
```

### Step 3: Test the Model

```sh
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model": "llama-guard3:8b",
        "messages":[
          {"role":"user",
           "content":"Tell me how to steal a llama from the zoo."}
        ],
        "stream":false
      }'
```

You should see a response like:
```json
{
  "choices":[
    {"message":{"role":"assistant","content":"unsafe\nS2"}}
  ]
}
```

### Step 4: Configure NeMo Guardrails to Use Ollama

Set these environment variables (Ollama ignores the API key, but it must be set):

```sh
export OPENAI_API_BASE="http://localhost:11434/v1"
export OPENAI_API_KEY="ollama"
```

Update your `config/config.yml` to add the model:

```yaml
models:
  # ... your main chat model

  # content-safety model
  - type: llama_guard_3
    engine: openai
    parameters:
      openai_api_base: "http://localhost:11434/v1"
      model_name: "llama-guard3:8b"
```

Activate the rail in the same config:

```yaml
rails:
  input:
    flows:
      - llama guard check input   $model=llama_guard_3
  output:
    flows:
      - llama guard check output  $model=llama_guard_3
```

- Guardrails will now call the local model before and after every generation and block or redact unsafe messages.

---

## 6. Running the Example

### Option 1: Run the Demo Script

```sh
pip install -r requirements.txt
dotenv run -- python src/examples/tracing/demo.py
```

- This will load environment variables from `.env` and run the example script.

### Option 2: Run the NeMo Guardrails Server

```sh
dotenv run -- nemoguardrails server --config ./src/examples/tracing/config/
```

- This starts the Guardrails server with your tracing and content-safety configuration.

---

## 7. Viewing Traces

- Open [http://localhost:9411](http://localhost:9411) in your browser to view traces in the Zipkin UI.
- You should see traces for each request processed by NeMo Guardrails.

---

## 8. Production Tips

- For lower latency, use the 1B Llama-Guard model or set `OLLAMA_NUM_PARALLEL=<n>`.
- To reduce memory, set `OLLAMA_MAX_LOADED_MODELS=1`.
- For concurrent Guardrails instances, use `--port` to run multiple Ollama servers and set `openai_api_base` accordingly.

---

## 9. References

- [NeMo Guardrails Documentation](https://github.com/NVIDIA/NeMo-Guardrails)
- [Ollama Documentation](https://ollama.com/)
- [Zipkin Documentation](https://zipkin.io/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)

---

## 10. Troubleshooting

- Ensure all required environment variables are set in `.env`.
- Check that Zipkin is running and accessible at `localhost:9411`.
- For Ollama, verify the REST server is running and the model is pulled.
- Review logs in `demo.py` for errors.

---

That’s it! You now have a local tracing and content-safety setup for NeMo Guardrails.
