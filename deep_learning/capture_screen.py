from VividClient import *

client = VividClient(ip='192.168.0.11', port=16601)

responses = client.simGetImages([
	ImageRequest(0, AirSimImageType.Scene),
	ImageRequest(1, AirSimImageType.DepthPlanner, True),
	ImageRequest(0, AirSimImageType.DepthVis),
	ImageRequest(0, AirSimImageType.Segmentation),
	ImageRequest(1, AirSimImageType.Segmentation, True),
	ImageRequest(0, AirSimImageType.SurfaceNormals)])

for i, response in enumerate(responses):
	if response.pixels_as_float:
		print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
		VividClient.write_pfm(os.path.normpath('./screenshot_' + str(i) + '.pfm'), VividClient.getPfmArray(response))
	else:
		print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
		VividClient.write_file(os.path.normpath('./screenshot_' + str(i) + '.png'), response.image_data_uint8)

# Get uncompressed image bytes and show RGBA data
from matplotlib import pyplot as PLT
resp = client.simGetImages([ImageRequest(0, AirSimImageType.Scene, False, False)])
img = np.array(bytearray(resp[0].image_data_uint8)).reshape(144, 256, 4)
PLT.imshow(img)
PLT.show()
