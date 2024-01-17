using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main()
    {
        string url = "https://honkaistarrailbot.herokuapp.com/api/card";
        string json = @"{
            ""uid"": ""Your_UID"",
            ""lang"": ""ua"",
            ""name"": ""1208, 1205, 1112"",
            ""image"": {
                ""1302"": ""https://i.pximg.net/img-master/img/2023/06/20/16/53/28/109183352_p0_master1200.jpg""
            }
        }";

        using (HttpClient client = new HttpClient())
        using (HttpContent content = new StringContent(json, Encoding.UTF8, "application/json"))
        using (HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, url))
        {
            request.Content = content;

            HttpResponseMessage response = await client.SendAsync(request);

            if (response.IsSuccessStatusCode)
            {
                string responseData = await response.Content.ReadAsStringAsync();
                Console.WriteLine("Request successful");
                Console.WriteLine(responseData);
            }
            else
            {
                Console.WriteLine($"Request failed with status code {response.StatusCode}");
            }
        }
    }
}

