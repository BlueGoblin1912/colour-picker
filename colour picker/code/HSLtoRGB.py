import math
def HSLtoRGB(hue,saturation,luminosity):
    if luminosity < 0.5:
        temp1 = luminosity*(saturation+1)
    else:
        temp1= luminosity+saturation-(luminosity*saturation)
    temp2 = 2*luminosity-temp1
    Hue= hue/360
    Rt = Hue + 1/3 
    Gt = Hue
    Bt = Hue - 1/3

    if Rt < 0:
        Rt += 1
    elif Rt > 1:
        Rt -= 1
    if Gt < 0:
        Gt += 1
    elif Gt > 1:
        Gt -= 1
    if Bt < 0:
        Bt += 1
    elif Bt > 1:
        Bt -= 1

    #red
    if 6*Rt < 1:
        Red = temp2+(temp1-temp2)*6*Rt
    elif 2*Rt < 1:
        Red = temp1
    elif 3*Rt < 2:
        Red = temp2+(temp1-temp2)*(2/3-Rt)*6
    else:
        Red = temp2

    #green
    print(temp1,temp2,Gt)
    if 6*Gt < 1:
        Green = temp2+(temp1-temp2)*6*Gt
    elif 2*Gt < 1:
        Green = temp1
    elif 3*Gt < 2:
        Green = temp2+(temp1-temp2)*(2/3-Gt)*6
        print(Green)
    else:
        Green = temp2
    
    #blue
    if 6*Bt < 1:
        Blue = temp2+(temp1-temp2)*6*Bt
    elif 2*Bt < 1:
        Blue = temp1
    elif 3*Bt < 2:
        Blue = temp2+(temp1-temp2)*(2/3-Bt)*6
    else:
        Blue = temp2

    Red *= 255
    Green *= 255
    Blue *= 255

    return round(Red),round(Green),round(Blue)

def RGBtoHue(r,g,b):
    R = r/255
    G = g/255
    B = b/255
    if R > G and R > B:#R is the largest
        Hue = (G-B)/(R-min(G,B))
    elif G > R and G > B:#G is the largest
        Hue = 2 + (B-R)/(G-min(B,R))
    else:#B is the largest
        Hue = 4 +(R-G)/(B-min(R,G))
    
    Hue = Hue * 60
    if Hue < 0:
        Hue += 360
    return Hue
print(HSLtoRGB(RGBtoHue(24,98,118),0.67,0.28))
