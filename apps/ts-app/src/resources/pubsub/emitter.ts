import * as events from "events"

/**
 * @klotho:disabled::pubsub {
 *   id = "pubsub-emitter"
 * }
 */
export const pubsubEmitter = new events.EventEmitter();