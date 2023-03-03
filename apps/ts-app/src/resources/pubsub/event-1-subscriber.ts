import {pubsubEmitter} from "./emitter";

import {Event} from "./models";

export function subscribeToEvent1() {
    pubsubEmitter.on('event-1', async (event: Event) => {
        console.log(`handling event event: ${JSON.stringify(event)}`)
        console.log(`triggering event-2 for event id:${event.id}`)
        pubsubEmitter.emit("event-2", {id: event.id, payload: `${event.payload}-response`});
    });
}
