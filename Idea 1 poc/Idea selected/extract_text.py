import sys
import Quartz
import Vision
from Cocoa import NSURL

def extract_text(image_path):
    input_url = NSURL.fileURLWithPath_(image_path)
    
    request = Vision.VNRecognizeTextRequest.alloc().init()
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    
    handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(input_url, None)
    
    success, error = handler.performRequests_error_([request], None)
    
    if success:
        text = "\n".join([obs.topCandidates_(1)[0].string() for obs in request.results()])
        print(text)
    else:
        print(f"Error: {error}")

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        print(f"--- {arg} ---")
        extract_text(arg)
