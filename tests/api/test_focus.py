from fastapi.testclient import TestClient
from main import app

client=TestClient(app)



fake_db = {
  "focus": [
    {
      "id": 1,
      "focus_name": "Cybersecurity Threats in Critical Infrastructure",
      "reports": [
        {
          "country": "USA",
          "description": "Increased ransomware attacks on energy and transportation sectors; mitigation measures include enhanced threat intelligence sharing and mandatory reporting of incidents.",
          "created_at": "2025-10-28T18:00:00"
        },
        {
          "country": "UK",
          "description": "Phishing and supply-chain attacks targeting government agencies and healthcare systems.",
          "created_at": "2025-10-27T14:00:00"
        }
      ]
    },
    {
      "id": 2,
      "focus_name": "Border Tensions and Military Build-up",
      "reports": [
        {
          "country": "Ukraine",
          "description": "Russian troop movement detected along the eastern border; increased surveillance recommended.",
          "created_at": "2025-10-28T17:30:00"
        },
        {
          "country": "Poland",
          "description": "Border patrols increased near Belarus following airspace violation reports.",
          "created_at": "2025-10-26T15:10:00"
        }
      ]
    }
  ]
}


def test_get_focus():
    response = client.get("/api/focus/1")
    assert response.status_code == 200
    data = response.json
    assert response.json()=={
        "focus_id": 1,
        "focus_name": "Cybersecurity Threats in Critical Infrastructure",
        "reports": [
            {
            "country": "USA",
            "description": "Increased ransomware attacks on energy and transportation sectors; mitigation measures include enhanced threat intelligence sharing and mandatory reporting of incidents.",
            "created_at": "2025-10-28T18:00:00"
            },
            {
            "country": "UK",
            "description": "Phishing and supply-chain attacks targeting government agencies and healthcare systems.",
            "created_at": "2025-10-27T14:00:00"
            }
        ]
    }
