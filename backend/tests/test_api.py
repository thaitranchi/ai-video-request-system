from fastapi.testclient import TestClient
from app.main import app  # Adjusted import based on your app location
from unittest.mock import AsyncMock, patch

def test_create_request(mocker):
    # Mock the entire video_pipeline.process_request to prevent actual processing
    # and external calls (DB, file system, TTS, FFmpeg).
    # This allows us to test the API endpoint's immediate response.
    with patch("app.api.routes.requests.video_pipeline.process_request", new_callable=AsyncMock) as mock_process_request:
        # Configure the mock to return None or a specific value if needed
        mock_process_request.return_value = None

        client = TestClient(app)
        response = client.post("/api/v1/requests", json={
            "query": "What is the chemical formula for water?",
            "language": "en"
        })
        
        assert response.status_code == 202
        assert response.json()["status"] == "pending"

        # Assert that video_pipeline.process_request was called with the correct arguments
        # Use positional arguments to match the actual call in the route handler
        mock_process_request.assert_called_once_with(
            mocker.ANY, 
            "What is the chemical formula for water?"
        )

    # The openai_service.generate_video_script mock is no longer needed here
    # because we are mocking the higher-level process_request function.