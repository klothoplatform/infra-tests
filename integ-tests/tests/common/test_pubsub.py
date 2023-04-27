import uuid

import pytest

from tests import session
from tests.util import resolve_primary_gw_url


@pytest.mark.skip(reason="not implemented in IFC2")
@pytest.mark.ts_app
@pytest.mark.common
def test_pubsub_event():
    event_id = str(uuid.uuid4())
    event_payload = str(uuid.uuid4())
    event = {"id": event_id, "payload": event_payload}
    response = session.post(resolve_primary_gw_url("test/pubsub/pubsub-event"), json=event)
    assert response.status_code == 200
    assert response.json() == {"id": event_id, "payload": f"{event_payload}-response"}
