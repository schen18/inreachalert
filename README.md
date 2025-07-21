# inReach River Warnings and Alerts

Something I whipped up for safety whilst doing solo multi-day hiking trips in canyons prone to flash flooding in the American Southwest. As there won't be any cell reception, I created this to allow me to regularly check river levels by sending a message via InReach satellite communicator to a Twilio number SMS service. In addition, if there were any flood warnings issued, Twilio would send me a SMS warning to my InReach number that will then get forwarded to my InReach device via satellite.

The Flask app pulls river levels data, as well as river flood warnings. See Twilio screenshot on how to wire up the app response with your Twilio number.
