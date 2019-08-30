from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from plant.models import *
from plant.forms import *
from django.shortcuts import redirect
from django.views.generic import TemplateView,ListView
import time

def diaryview(request, pk):
    plant = Diary.objects.get(user_id=pk)
    photo = SeedState.objects.get(growth_id=1, seed_id=1)
    form = PlantForm(request.POST, instance=plant)
    if form.is_valid():
        plant = form.save(commit=True)
        plant.save()
        if plant.exp <= 5:
            # 회원 작물일지
            plant =  Diary.objects.get(user_id=pk)
            # 회원 씨앗상태
            myseed = plant.seedState_id
            print(myseed)
            # 회원 씨앗상태의 씨앗번호
            seed = SeedState.objects.get(id=myseed).seed_id
            print(seed)
            # 회원 씨앗번호의 레벨1
            photo = SeedState.objects.get(growth_id=1, seed_id=seed)
        elif plant.exp <= 10:
            plant =  Diary.objects.get(user_id=pk)
            myseed = plant.seedState_id
            seed = SeedState.objects.get(id=myseed).seed_id
            photo = SeedState.objects.get(growth_id=2, seed_id=seed)
        elif plant.exp <= 15:
            plant =  Diary.objects.get(user_id=pk)
            myseed = plant.seedState_id
            seed = SeedState.objects.get(id=myseed).seed_id
            photo = SeedState.objects.get(growth_id=3, seed_id=seed)
        elif plant.exp <= 20:
            plant = Diary.objects.get(user_id=pk)
            myseed = plant.seedState_id
            seed = SeedState.objects.get(id=myseed).seed_id
            photo = SeedState.objects.get(growth_id=4, seed_id=seed)
        else:  # 다 자랐을 때
            plant = Diary.objects.get(user_id=pk)
            photo = SeedState.objects.get(growth_id=1, seed_id=1)
            return render(request, 'plant/userplant.html', {'plant': plant, 'photo':photo})
    else:
        form = PlantForm(instance=plant)
        # return redirect('home')
    return render(request, 'plant/userplant.html', {'form': form, 'plant': plant, 'photo':photo})


# 190719_시인 - 190726 예림 불필요 view 삭제
def my_diaryview(request, pk):
  # diarys = get_object_or_404(user_id=uk)
  diarys = Diary.objects.filter(user_id=pk)
  return render(request, 'plant/jakmulDiary.html', {'diarys': diarys})

# 190726 소희
class seedinfo(ListView):
    template_name = 'plant/seedinfo.html'
    context_object_name = 'seeds'
    model = Seed

# 7.21 소이 - 배송신청에 마이페이지 내용 불러옴 / 0812 예림 수정
def delivery_profile(request, uk):
    user_donation_id = Diary.objects.filter(user_id=uk).last().donation_id
    user_donation= DonationOrg.objects.get(id=user_donation_id)
    user_seedState_id = Diary.objects.filter(user_id=uk).last().seedState_id
    user_seed_id = SeedState.objects.get(id=user_seedState_id).seed_id
    user_seed = Seed.objects.get(id=user_seed_id)
    if request.method == 'POST' and 'update' in request.POST:
        form = profileForm(data=request.POST, instance=request.user)
        update = form.save(commit=False)
        update.user = request.user
        update.save()
    elif request.method == 'POST' and 'delivery_start' in request.POST:
        user_delivery = Diary.objects.filter(user_id=uk).last()
        user_delivery.delivery = '배송 중'
        user_delivery.save()
        return redirect('plant:jakmulDiary', pk=uk)
    else:
        form = profileForm(instance=request.user)
    return render(request, 'plant/delivery.html', {'form': form, 'user_donation':user_donation, 'user_seed':user_seed})


# 7.25 소이 - 기부단체 선택 / 8.12 예림 수정
def org_select(request, uk):
    donationOrgs = DonationOrg.objects.filter(is_donate=1)
    if request.method == "POST" and 'donate1' in request.POST:
        print("donate1버튼 누름")
        user_donation = Diary.objects.filter(user_id=uk).last()
        user_donation.donation_id = donationOrgs.filter(is_donate=1)[0]
        user_donation.save()
        return redirect('plant:delivery', uk=uk)
    elif request.method == "POST" and 'donate2' in request.POST:
        print("donate2버튼 누름")
        user_donation = Diary.objects.filter(user_id=uk).last()
        user_donation.donation_id = donationOrgs.filter(is_donate=1)[1]
        user_donation.save()
        return redirect('plant:delivery', uk=uk)
    elif request.method == "POST" and 'donate3' in request.POST:
        print("donate3버튼 누름")
        user_donation = Diary.objects.filter(user_id=uk).last()
        user_donation.donation_id = donationOrgs.filter(is_donate=1)[2]
        user_donation.save()
        return redirect('plant:delivery', uk=uk)
    return render(request, 'plant/donation_select.html', {'donationOrgs': donationOrgs})

# 작물 게임 - 190802 예림 / 190813 예림 수정
# 화면에 나타나는 것: 레벨, 경험치바, 작물상태(목마름), 작물사진, 도구, 도구 개수
def plantgame(request, pk):
    try:
        if Diary.objects.filter(user_id=pk).last().donation_id is None:
            # 회원 일지
            user_diary = Diary.objects.get(user_id=pk, donation_id=None)
            # 저장된 작물 상태
            plantState = PlantState.objects.get(id=user_diary.plantState_id)
            # 씨앗 상태
            user_seedState = SeedState.objects.get(id=user_diary.seedState_id)
            # 도구 부족 알림
            def need(a):
                    need = Item.objects.get(id=a).name + "부족"
                    return need
            # 작물 상태 - 도구 비교, 작물상태 랜덤
            def game(a, plantState, user_diary):
                # 저장된 작물 상태에 맞는 도구
                psitem = PlantState.objects.get(id=user_diary.plantState_id).item_id
                # 도구가 부족할 때
                if HaveItem.objects.get(user_id=pk, item_id=a).item_count <= 0:
                    need = Item.objects.get(id=a).name + "부족"
                    print(need)
                    return need
                # 작물 상태와 도구가 맞을 때
                if psitem == a:
                    print("맞습니다.")
                    # 아이템 썼을 때 줄어들기
                    user_items_count = HaveItem.objects.get(user_id=pk, item_id=a)
                    user_items_count.item_count = user_items_count.item_count - 1
                    user_items_count.save()
                    # 경험치 +
                    user_diary.exp = user_diary.exp + plantState.change_exp
                    user_diary.save()
                    # 작물 상태(랜덤으로 하나)
                    plantState = PlantState.objects.all().order_by('?').first()
                    print(plantState.state, plantState.id)
                    # 현재 작물 상태 저장
                    user_diary.plantState_id = plantState.id
                    user_diary.save()
                # 틀렸을 때
                else:
                    print("틀렸습니다.")
            # 도구 버튼 눌렀을 때
            if request.method == "POST" and 'item1' in request.POST:
                print("item1 버튼 누름", Item.objects.get(id=1).id)
                if HaveItem.objects.get(user_id=pk, item_id=1).item_count <= 0:
                    need = need(1)
                else:
                    game(1, plantState, user_diary)
            elif request.method == "POST" and 'item2' in request.POST:
                print("item2 버튼 누름", Item.objects.get(id=2).id)
                if HaveItem.objects.get(user_id=pk, item_id=2).item_count <= 0:
                    need = need(2)
                else:
                    game(2, plantState, user_diary)
            elif request.method == "POST" and 'item3' in request.POST:
                print("item3 버튼 누름", Item.objects.get(id=3).id)
                if HaveItem.objects.get(user_id=pk, item_id=3).item_count <= 0:
                    need = need(3)
                else:
                    game(3, plantState, user_diary)
            elif request.method == "POST" and 'item4' in request.POST:
                print("item4 버튼 누름", Item.objects.get(id=4).id)
                if HaveItem.objects.get(user_id=pk, item_id=4).item_count <= 0:
                    need = need(4)
                else:
                    game(4, plantState, user_diary)
            elif request.method == "POST" and 'item5' in request.POST:
                print("item5 버튼 누름", Item.objects.get(id=5).id)
                if HaveItem.objects.get(user_id=pk, item_id=5).item_count <= 0:
                    need = need(5)
                else:
                    game(5, plantState, user_diary)
            # 표시되는 레벨과 경험치
            level = user_diary.exp // 100 + 1
            if user_diary.exp < 100:
                user_exp = user_diary.exp
            elif user_diary.exp - ((level - 2) * 100) == 100:
                user_exp = 0
            else:
                user_exp = user_diary.exp - ((level - 1) * 100)
            # 회원이 가진 도구
            i = 1
            items = []
            while i <= HaveItem.objects.filter(user_id=pk).count():
                a = []
                item = Item.objects.get(id=i)
                user_items_count = HaveItem.objects.get(user_id=pk, item_id=i)
                a.append(item)
                a.append(user_items_count)
                items.append(a)
                i = i + 1
            if request.method == "POST" and 'growth_btn' in request.POST:
                user_seed = SeedState.objects.get(id=user_seedState.id).seed_id
                user_growth = SeedState.objects.get(id=user_seedState.id).growth_id
                user_diary.seedState_id = SeedState.objects.get(seed_id=user_seed, growth_id=user_growth+1)
                user_diary.exp = user_diary.exp + 10
                user_diary.save()
                return redirect('plant:userplant', pk=pk)
            if request.method == "POST" and 'harvest' in request.POST:
                user = User.objects.get(id=pk)
                rank = Rank.objects.get(id=user.rank_id)
                user.ticket = user.ticket + rank.ticket
                user.save()
                return render(request, 'plant/harvest.html', {'pk':pk})
            plantState = PlantState.objects.get(id=user_diary.plantState_id)
            return render(request, 'plant/userplant.html',
                          {'plantState': plantState, 'user_seedState':user_seedState,
                           'user_exp': user_exp, 'level':level, 'items':items, 'user_diary':user_diary,
                           'need':need
                           })
        # 다시 작물 시작
        else:
            return redirect('plant:selectSeed', pk=pk)

    # 처음 작물시작
    except AttributeError:
        items = Item.objects.all()
        for i in items:
            user_items = HaveItem.objects.create(item_count=0, item_id=i.id, user_id=pk)
            user_items.save()
        return redirect('plant:selectSeed', pk=pk)

def selectSeed(request, pk):
    selectSeeds = Seed.objects.all()
    def select(a):
        user_seedState = SeedState.objects.get(seed_id=a, growth_id=1).id  # plant_seedState테이블의 조건을 만족하는 id 행을 가져옴
        user_seed_id = Diary.objects.create(delivery=None, donation=None, seedState_id=user_seedState, user_id=pk,
                                            plantState_id=1)
        user_seed_id.save()

    if request.method == 'POST' and 'seed1' in request.POST:
        print("seed1누름")
        select(1)
        return redirect('plant:userplant', pk=pk)
    elif request.method == 'POST' and 'seed2' in request.POST:
        select(2)
        return redirect('plant:userplant', pk=pk)
    elif request.method == 'POST' and 'seed3' in request.POST:
        select(3)
        return redirect('plant:userplant', pk=pk)
    elif request.method == 'POST' and 'seed4' in request.POST:
        select(4)
        return redirect('plant:userplant', pk=pk)
    elif request.method == 'POST' and 'seed5' in request.POST:
        select(5)
        return redirect('plant:userplant', pk=pk)
    return render(request, 'plant/selectSeed.html', {'selectSeeds': selectSeeds})
