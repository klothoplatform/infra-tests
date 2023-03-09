using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;

// @klotho::embed_assets {
//  id = "embedded-assets"
//  include = ["/embedded-assets/**/*.txt"]
//  exclude = ["**/excluded-text.txt"]
// }

namespace SampleApp
{
  /**
   * @klotho::execution_unit {
   *   id ="executor"
   * }
   */
  public class Startup
  {
    public void ConfigureServices(IServiceCollection services)
    {
      services.AddControllers();
    }

    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
      app.UseRouting();
      
      /**
       * @klotho::expose {
       *   id = "gateway-primary"
       *   target = "public"
       * }
       */
      app.UseEndpoints(endpoints =>
      {
        endpoints.MapControllers();
      });
    }
  }
}
