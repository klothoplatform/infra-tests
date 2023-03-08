
export function testHandlesPathParams(req, res) {
    res.send(req.params.param);
}