import Foundation
import Vision
import CoreImage

let args = CommandLine.arguments
guard args.count == 3 else { print("usage: bg-remove <input> <output.png>"); exit(1) }
let inURL = URL(fileURLWithPath: args[1])
let outURL = URL(fileURLWithPath: args[2])
guard let ciImage = CIImage(contentsOf: inURL) else { print("ERROR load"); exit(1) }

let request = VNGenerateForegroundInstanceMaskRequest()
let handler = VNImageRequestHandler(ciImage: ciImage)
do { try handler.perform([request]) } catch { print("ERROR vision \(error)"); exit(2) }
guard let result = request.results?.first else { print("ERROR no fg"); exit(3) }

let maskBuffer: CVPixelBuffer
do { maskBuffer = try result.generateScaledMaskForImage(forInstances: result.allInstances, from: handler) }
catch { print("ERROR mask \(error)"); exit(4) }

let maskCI = CIImage(cvPixelBuffer: maskBuffer)
let clearBG = CIImage(color: CIColor.clear).cropped(to: ciImage.extent)
guard let filter = CIFilter(name: "CIBlendWithMask") else { exit(5) }
filter.setValue(ciImage, forKey: kCIInputImageKey)
filter.setValue(clearBG, forKey: kCIInputBackgroundImageKey)
filter.setValue(maskCI, forKey: kCIInputMaskImageKey)
guard let output = filter.outputImage else { print("ERROR blend"); exit(6) }

let context = CIContext()
guard let srgb = CGColorSpace(name: CGColorSpace.sRGB) else { exit(7) }
do { try context.writePNGRepresentation(of: output, to: outURL, format: .RGBA8, colorSpace: srgb); print("OK") }
catch { print("ERROR write \(error)"); exit(8) }
