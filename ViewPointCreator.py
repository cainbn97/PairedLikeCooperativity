import pymol
import numpy as np

cmd.delete("*pair*")
cmd.hide("everything", "all")



for object in cmd.get_object_list():
	print("Starting " + str(object))

	cmd.show("cartoon", object)

	## ViewPoint 1: Helix 1 and 2
	cmd.set_view((-0.6168535351753235, 0.7621465921401978, 0.19653142988681793, 0.7778617739677429, 0.6284170150756836, 0.004479607101529837, -0.12009003758430481, 0.15563763678073883, -0.9804883599281311, -0.0002382512902840972, -0.0002788156270980835, -84.81782531738281, 21.37558937072754, 114.3082046508789, -11.685637474060059, 76.26731872558594, 93.36870574951172, -20.0))

	cmd.set("label_size", 24)
	cmd.distance(f"{object}_pair12_38", f"/{object}/A/A/12/CA", f"/{object}/A/A/38/CA")
	cmd.color("gray", f"{object}_pair12_38")

	cmd.distance(f"{object}_pair15_34", f"/{object}/A/A/15/CA", f"/{object}/A/A/34/CA")
	cmd.color("gray", f"{object}_pair15_34")

	cmd.distance(f"{object}_pair19_30", f"/{object}/A/A/19/CA", f"/{object}/A/A/30/CA")
	cmd.color("gray", f"{object}_pair19_30")

	cmd.distance(f"{object}_pair22_29", f"/{object}/A/A/22/CA", f"/{object}/A/A/29/CA")
	cmd.color("gray", f"{object}_pair22_29")

	cmd.ray(1600, 1600)
	cmd.png(f"{object}_Helix1and2ViewPoint.png", dpi=600)

	cmd.delete("*pair*")


	## Viewpoint 2: Helix 1 and 3
	cmd.set_view((-0.8361549377441406, 0.1676131933927536, 0.5222470164299011, -0.48889607191085815, 0.2038549929857254, -0.8481840491294861, -0.24863260984420776, -0.9645398855209351, -0.08851101249456406, 0.0005135359242558479, -0.0006188042461872101, -53.184871673583984, 25.726604461669922, 110.406005859375, -6.873864650726318, 31.849241256713867, 74.65108489990234, -20.0))

	cmd.set("label_size", 26)
	cmd.distance(f"{object}_pair13_48", f"/{object}/A/A/13/CA", f"/{object}/A/A/48/CA")
	cmd.color("gray", f"{object}_pair13_48")

	cmd.distance(f"{object}_pair16_45", f"/{object}/A/A/16/CA", f"/{object}/A/A/45/CA")
	cmd.color("gray", f"{object}_pair16_45")

	cmd.distance(f"{object}_pair17_52", f"/{object}/A/A/17/CA", f"/{object}/A/A/52/CA")
	cmd.color("gray", f"{object}_pair17_52")

	cmd.distance(f"{object}_pair20_49", f"/{object}/A/A/20/CA", f"/{object}/A/A/49/CA")
	cmd.color("gray", f"{object}_pair20_49")

	cmd.ray(1600, 1600)
	cmd.png(f"{object}_Helix1and3ViewPoint.png", dpi=600)

	cmd.delete("*pair*")


	## Viewpoint 3: Helix 2 and 3

	cmd.set_view((0.8304816484451294, 0.19060321152210236, -0.5234038233757019, 0.4968070387840271, 0.17150701582431793, 0.8507378101348877, 0.25192493200302124, -0.966554582118988, 0.04774308577179909, -0.0007469318807125092, -0.0011044926941394806, -64.79312133789062, 21.725807189941406, 111.02168273925781, -6.777954578399658, 41.400821685791016, 88.12902069091797, -20.0))
	
	cmd.set("label_size", 26)
	
	cmd.distance(f"{object}_pair31_42", f"/{object}/A/A/31/CA", f"/{object}/A/A/42/CA")
	cmd.color("gray", f"{object}_pair31_42")

	cmd.distance(f"{object}_pair32_42", f"/{object}/A/A/28/CA", f"/{object}/A/A/46/CA")
	cmd.color("gray", f"{object}_pair32_42")

	cmd.distance(f"{object}_pair35_42", f"/{object}/A/A/35/CA", f"/{object}/A/A/42/CA")
	cmd.color("gray", f"{object}_pair35_42")

	cmd.distance(f"{object}_pair34_45", f"/{object}/A/A/34/CA", f"/{object}/A/A/45/CA")
	cmd.color("gray", f"{object}_pair34_45")


	cmd.ray(1600, 1600)
	cmd.png(f"{object}_Helix2and3ViewPoint.png", dpi=600)

	cmd.delete("*pair*")

	


	cmd.hide("everything", "all")

	



print('DONE!')
