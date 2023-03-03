import {pubsubEmitter} from "./emitter";

import * as kvMap from "../persist/kv-map"
import {Event} from "./models";
import {subscribeToEvent1} from "./event-1-subscriber";

/**
 * @klotho::execution_unit {
 *   id = "event-1-subscriber"
 * }
 */

subscribeToEvent1();

export function subscribeToEvent2(res) {
    pubsubEmitter.on('event-2', async (event: Event) => {
        console.log(`handling event event: ${JSON.stringify(event)}`);
        pubsubEmitter.removeAllListeners("event-2");
        res.json(event);
    });
}
