using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace SampleApp.Controllers
{
    [Route("/test/embed-assets")]
    public class EmbedAssetsController : ControllerBase
    {
        private IHostingEnvironment Environment;

        public EmbedAssetsController(IHostingEnvironment _environment)
        {
            Environment = _environment;
        }
        
        [HttpGet("get-asset")]
        public ActionResult TestGetEmbeddedAsset([FromQuery(Name = "path")] string path)
        {
            try
            {
                Stream stream = System.IO.File.OpenRead(Path.Combine(Environment.ContentRootPath, path));
                var mimeType = MimeTypeMap.List.MimeTypeMap.GetMimeType(Path.GetExtension(path))
                    .FirstOrDefault("text/plain");

                return new FileStreamResult(stream, mimeType)
                {
                    FileDownloadName = Path.GetFileName(Path.Combine(Environment.ContentRootPath, path))
                };
            }
            catch (FileNotFoundException)
            {
                return new NotFoundResult();
            }
        }
    }
}