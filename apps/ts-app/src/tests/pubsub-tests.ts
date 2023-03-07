import {pubsubEmitter} from "../resources/pubsub/emitter";
import {Event} from "../resources/pubsub/models";
import {respondWithEventTwo} from "../resources/pubsub/events";



export async function testPubSubEvent(req, res) {
    respondWithEventTwo(res)
    pubsubEmitter.emit("event-1", req.body as Event);
}

