from django.utils.deprecation import MiddlewareMixin

class AuthMD(MiddlewareMixin):
    while_list = ['/userlogin/']
    black_list = ['/black/']

    def process_request(self,request):
        from django.shortcuts import redirect,HttpResponse

        next_url = request.path_info
        print(request.path_info,request.get_full_path())
        
        if next_url in self.black_list:
            return HttpResponse('This is an illegal url')
        elif next_url in self.while_list or request.session.get('user'):
            return
        else:
            return redirect("/userlogin/?next={}".format(next_url))
        