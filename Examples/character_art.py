import asyncio
import starrailcard

character_art = {
    "1302": "https://media1.tenor.com/m/FEb6-ok4RVcAAAAC/honkai-star.gif",
    "1305": "https://i.ibb.co/Sv6kY41/imgonline-com-ua-Pic-On-Pic-STp-FV0-Drb-VG1-Wf-Pb.jpg",
    "1205": "https://i.pximg.net/img-master/img/2023/08/06/00/00/50/110562032_p0_master1200.jpg",
    "1211": "https://i.pximg.net/img-master/img/2023/05/25/01/31/57/108415268_p1_master1200.jpg",
    "1006": "https://i.ibb.co/M7f4Xvg/109206813-p2-master1200.png",
    "1307": "https://i.pximg.net/img-master/img/2024/02/11/00/18/25/115939009_p0_master1200.jpg",
    "1102": "https://i.ibb.co/MfmDcmh/108269946-p0-master1200.jpg",
    "1112": ["https://i.pximg.net/img-master/img/2023/11/09/10/35/56/113260471_p0_master1200.jpg","https://i.pximg.net/img-master/img/2024/01/21/17/15/18/115358703_p0_master1200.jpg"],
}

async def main():
    async with starrailcard.MiHoMoCard(character_art = character_art) as card:
        print(card)
        
asyncio.run(main())
