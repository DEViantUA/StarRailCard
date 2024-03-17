import asyncio
import starrailcard

async def main():
    image = await starrailcard.is_valid_image("https://i.pximg.net/img-master/img/2024/01/21/17/15/18/115358703_p0_master1200.jpg", headers = starrailcard.get_pixv_headers())
    print(image) #True
    
    image = await starrailcard.is_valid_image("https://i.pximg.net/img-master/img/2024/01/21/17/15/18/115358703_p0_master1200.jpg")
    print(image) #False
    
    image = await starrailcard.is_valid_image("https://github.com/DEViantUA/StarRailCard/tree/main/Examples")
    print(image) #False
    
    image = await starrailcard.is_valid_image("https://i.ibb.co/Sv6kY41/imgonline-com-ua-Pic-On-Pic-STp-FV0-Drb-VG1-Wf-Pb.jpg", headers = starrailcard.get_pixv_headers())
    print(image) #True
            
asyncio.run(main())
