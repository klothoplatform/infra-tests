// @klotho::static_unit {
//   id = "static-unit"
//   index_document	= "static-unit-index.html"
//   static_files = ["static-unit.js"]
// }
const nodeStatic = require('node-static');
const server = new nodeStatic.Server('./');

require('http').createServer(function (request, response) {
    request.addListener('end', function () {
            if (request.url === "/") {
                server.serveFile('/static-unit-index.html', 200, {}, request, response);
            } else {
                server.serve(request, response);
            }

    }).resume();
}).listen(4200);

console.log('Serving on http://localhost:4200/');
