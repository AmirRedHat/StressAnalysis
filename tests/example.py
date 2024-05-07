import sys
import os 

sys.path.append(os.path.dirname(os.path.dirname(os.path.join(__file__))))
from stressanalysis.base import StressAnalysis
from stressanalysis.job import send, send_parallel


class MyExample(StressAnalysis):
    
    request_timeout = 5
    
    @send(request_count=300, is_parallel=True, workers_count=30)
    def get_index(self):
        self.get(
            url="https://test.api.philia.vip/admin"
        )
        
    def get_some_url(self):
        self.get(
            url="https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop"
        )
        
    def post_index(self):
        self.post(
            "baseurl/index.html",
            {"data": 4}
        )
        
        
def test():
    app = MyExample()
    app.analysis()
    for key, value in app.get_endpoint_info().items():
        print(key, value)
        print("======================")
    # send_parallel("https://test.api.philia.vip/admin")
    
if __name__ == "__main__":
    test()