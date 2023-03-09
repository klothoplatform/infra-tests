using Microsoft.AspNetCore.Mvc;

namespace SampleApp.Controllers
{
    [Route("/test/expose")]
    public class ExposeController : ControllerBase
    {
        [HttpGet("handles-path-params/{param:minlength(1)}")]
        public string TestHandlesPathParams(string param)
        {
            return param;
        }
    }
}