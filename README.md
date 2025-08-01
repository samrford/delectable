# Delectable

A service takes a list of some of your favourite dishes, finds some similar dishes you might like based on them, then finds restaurants in the specified location that serve them. 

The request info is used to create multiple LLM prompts that retrieve the data, which is then processed and returned.

It uses Temporal to orchestrate a workflow.

## Setup

1.  **Start Temporal:**

    Open a terminal and run the Temporal development server:

    ```bash
    temporal server start-dev --db-filename dev.db
    ```

    Keep the Temporal Web UI open in your browser to see the workflow execution live: [http://localhost:8233](http://localhost:8233)

2.  **Start the Application Server:**

    In a new terminal, start the app:

    ```bash
    python main.py
    ```

3.  **Start the Temporal Worker:**

    In another new terminal, start the Temporal worker that will process the workflows:

    ```bash
    python run_worker.py
    ```

## Configuration

Before running the application, you need to set the `GEMINI_API_KEY` environment variable. This is required to authenticate with the Google Gemini API.

```bash
export GEMINI_API_KEY="your-api-key"
```

## Usage

1.  **Submit a Search Request:**

    Use `curl` or any API client to send a POST request to the `/search` endpoint.

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{
        "dishes": [
            "Lamb Tikka Dhansak",
            "Bahn mi",
            "Steak and ale pie"
        ],
        "dish_count": 3,
        "location": "London"
    }' http://localhost:8787/search
    ```

    The response will be a workflow ID, which you'll use in the next step.

2.  **Retrieve the Results:**

    Once the workflow has had a moment to run (you can watch its progress in the Temporal UI), use the workflow ID from the previous step to make a GET request to the `/result/{workflow_id}` endpoint.

    Replace `{id-from-result}` with the actual workflow ID.

    ```bash
    curl http://localhost:8787/result/{id-from-result}
    ```

    The response will contain the list of dishes and the restaurants where you can find them.

