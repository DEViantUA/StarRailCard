import asyncio
import starrailcard

async def main():
    image = await starrailcard.get_link_image("https://i.pximg.net/img-master/img/2024/01/21/17/15/18/115358703_p0_master1200.jpg", api_key= "e3114d9239b35aec4215740b51fb60e2ba")
    print("Data Info:")
    print(f"  ID: {image.data.id}")
    print(f"  Title: {image.data.title}")
    print(f"  URL Viewer: {image.data.url_viewer}")
    print(f"  URL: {image.data.url}")
    print(f"  Display URL: {image.data.display_url}")
    print(f"  Width: {image.data.width}")
    print(f"  Height: {image.data.height}")
    print(f"  Size: {image.data.size}")
    print(f"  Time: {image.data.time}")
    print(f"  Expiration: {image.data.expiration}")

    print("\nImage Info:")
    print(f"  Filename: {image.data.image.filename}")
    print(f"  Name: {image.data.image.name}")
    print(f"  MIME: {image.data.image.mime}")
    print(f"  Extension: {image.data.image.extension}")
    print(f"  URL: {image.data.image.url}")

    print("\nThumbnail Info:")
    print(f"  Filename: {image.data.thumb.filename}")
    print(f"  Name: {image.data.thumb.name}")
    print(f"  MIME: {image.data.thumb.mime}")
    print(f"  Extension: {image.data.thumb.extension}")
    print(f"  URL: {image.data.thumb.url}")

    print("\nMedium Info:")
    print(f"  Filename: {image.data.medium.filename}")
    print(f"  Name: {image.data.medium.name}")
    print(f"  MIME: {image.data.medium.mime}")
    print(f"  Extension: {image.data.medium.extension}")
    print(f"  URL: {image.data.medium.url}")

    print("\nDelete URL:")
    print(f"  {image.data.delete_url}")

    print("\nSuccess: ", image.success)
    print("Status: ", image.status)        
        
asyncio.run(main())
