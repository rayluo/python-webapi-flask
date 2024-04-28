import os
from flask import Flask
from identity.flask import ApiAuth  # Note: ApiAuth and Auth shall not coexist in the same file


app = Flask(__name__)
auth = ApiAuth(
    client_id=os.getenv("CLIENT_ID"),
    authority=os.getenv("AUTHORITY"),
    )

@app.route("/resource")
@auth.authorization_required(expected_scopes={  # Case-sensitive
    os.getenv("SCOPE"): f"api://{os.getenv('CLIENT_ID')}/{os.getenv('SCOPE')}",  # Note: Entra ID's token contains only the "path" of a full URI as scope
})
def resource(*, context):
    return {"content": f"top secret for {context}"}

