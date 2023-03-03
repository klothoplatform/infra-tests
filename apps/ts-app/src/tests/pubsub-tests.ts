import {pubsubEmitter} from "../resources/pubsub/emitter";
import {Event} from "../resources/pubsub/models";
import {subscribeToEvent2} from "../resources/pubsub/event-2-subscriber";

export function testPubSubEvent(req, res) {
    subscribeToEvent2(res);
    pubsubEmitter.emit("event-1", req.body as Event);

}

