"""English and code-switched phrase banks.

English in a Riyadh support queue is not one register. Three show up here
on purpose and they are mixed inside every theme:

* fluent professional English — the person who would write the same
  complaint to a bank;
* second-language English with the errors that actually occur —
  "since one hour", dropped articles, "kindly", present tense for past,
  "he not find my villa". These are transcribed as errors, not corrected;
* phone-notes English — no capitals, full stops instead of clauses,
  the shape of something typed one-handed at the door.

"captain" is the ordinary English word for a delivery driver here, the
way "كابتن" is in the Arabic bank. "driver" and "delivery guy" appear
too. Spelling is deliberately inconsistent between tickets
(behaviour/behavior, cancelled/canceled) the way a real queue is.

The MIXED bank is the common real case, and it has a grammar. Riyadh
code-switching is *insertional*: the sentence frame is Arabic and the
matrix language supplies the function words and the finite verbs. What
gets borrowed is content — nouns, the occasional adjective, and strings
lifted verbatim off a screen. Four shapes account for nearly all of it:

1. Arabic frame, English product or technical noun dropped in, usually
   carrying the Arabic definite article: الـ app، الـ refund،
   الـ location، الـ update. The noun stays English because that is
   what the button says. Arabic proclitics attach to it directly —
   وعدتوني بـ refund.
2. A quoted UI string, kept in the language it appears in and then
   argued with: التطبيق يقول arriving soon من ساعه، وش يعني soon عندكم؟
3. Quoted speech — what the captain actually said, in the language he
   said it in: سألته وين وصلت فقال لي بالحرف not my problem.
4. A clause-boundary switch, where the speaker turns from describing to
   complaining and the whole frame flips.

What this bank deliberately does *not* do, because Saudi speakers do not
do it and it is the tell of machine-mixed text:

* English function words governing Arabic — no "because of التاخير".
  The subordinator comes from the matrix language: بسبب.
* Bare English finite verbs heading an Arabic clause — no "waited ساعه",
  no "cancelled الطلب". Either the verb stays Arabic (نزلته) or it is
  borrowed as a light-verb construction: سويت install، سويت uninstall.
* System morphemes from the embedded language — no "my address", no
  "kindly". Possessives and politeness markers come from Arabic.
* Calques — "on nothing" is not English; على الفاضي stays Arabic.

Dialect is Najdi throughout. The passive prefix is ان- (انخصم، انرفضت),
never the Egyptian/Levantine ات-.

Arabic script plus Latin script. Not Arabizi/Franco (3ashan, 7abibi) —
that is a different register and it would carry no Arabic characters at
all, which is both linguistically wrong for this queue and untestable.

Numbers are written both ways, Latin and Arabic-Indic, because both
appear on a Saudi keyboard and people do not standardise mid-sentence.

Deliberately, a theme's English, mixed and Arabic phrasings are not
translations of one another. A later task checks that all three cluster
together by theme; that check only means something if the three banks
arrived at the same complaint by different routes. If a MIXED entry is
its COLLOQUIAL sibling with two nouns flipped to English, a bag-of-words
model groups the two on shared Arabic tokens and never exercises the
cross-register skill the exercise exists to teach — so the entries here
say different things about the same grievance, and
``test_mixed_entries_diverge_from_their_arabic_siblings`` holds the line.

Keys mirror ``spec.THEMES`` exactly; the theme keys are defined there and
only there.
"""

ENGLISH = {
    "driver_lost": [
        "Driver couldn't find building, called me 4 times",
        "The captain got lost and blamed the map pin",
        "Driver said the location in the app is wrong, took him 30 min",
        "He ended up on a completely different street and I had to walk out "
        "to the main road to find him",
        "captain called 3 time and still he not find my villa",
        "Since you changed the address screen the pin drops in the wrong "
        "place every single time",
        "captain lost. 20 min circling. had to go down myself.",
        "My address is saved correctly but the app sends the captain to "
        "another district entirely",
        "Kindly fix your map, every captain is confused with my compound gate",
        "Third order in a row where the captain cannot find the apartment. "
        "Nothing changed on my side.",
        "The pin is on my building but he was standing in front of another "
        "tower asking me to come out",
        "delivery guy gave up and went back to the restaurant with my food",
    ],
    "late": [
        "Order was over an hour late",
        "Waited 90 minutes, no update in the app",
        "Third late delivery this month and not one word of explanation",
        "I ordered since one hour and half and till now nothing arrive",
        "ETA has been stuck on 15 minutes for the last 40 minutes",
        "ordered 8pm. arrived 9:45. no explanation, no apology.",
        "The restaurant finished the food ages ago and the captain only "
        "picked it up now",
        "Half an hour is what you promise. Reality is nothing close to that.",
        "Very slow delivery and no one from support answer me the whole time",
        "sooooo late, my guests already left",
        "Order sat in preparing for an hour and there is nobody to call",
    ],
    "wrong_items": [
        "Received someone else's order",
        "Two items missing from my order",
        "Ordered chicken, got beef",
        "Invoice says 4 items, the bag had 3",
        "They forget the drinks again even I write it in the notes",
        "wrong bag. different name on the receipt. not my food.",
        "The dessert I paid for was not in the bag and nobody refunded it",
        "I asked for no onion and it came loaded with onion, my son can't "
        "eat any of it",
        "Half the order missing and the captain had already driven off",
        "Got a different household's order completely, I hope they got mine",
    ],
    "cold_food": [
        "Food arrived completely cold",
        "Fries were soggy and the burger was cold",
        "Cold food because of the delay, again",
        "The soup was stone cold and the fat had set solid on top",
        "coffee came cold, juice came warm, everything the wrong temperature",
        "food cold. threw it away. paid 90 SAR for nothing.",
        "It left the restaurant hot and reached me an hour later stone cold",
        "Everything cold. I think the captain had two other orders before mine.",
        "the food was cold and the taste changed, we did not eat it",
    ],
    "payment_failed": [
        "Charged twice for the same order",
        "Payment failed but money was deducted",
        "Card declined three times then charged anyway",
        "Bank SMS says the amount was taken but the order never went through",
        "my card work everywhere else but not in your app, why?",
        "double charge. same order number. 145 SAR twice.",
        "The payment screen throws an error code and tells me nothing else",
        "Tried two different cards, both failed, and both got charged",
        "Wallet balance was deducted and the order still shows as unpaid",
    ],
    "refund_delay": [
        "Still waiting for my refund after 10 days",
        "Refund was promised last week, nothing yet",
        "Order cancelled ages ago, money never came back",
        "You said 3 working days. It has been two weeks.",
        "every time I contact support they say under review, until when?",
        "no refund. 3 tickets opened. no reply to any of them.",
        "The amount has not returned to my card and I actually need it",
        "It has been a month and I am still chasing this myself",
        "You refunded me to a wallet I never asked for. I want it back on "
        "the card I paid with.",
    ],
    "app_crash": [
        "App crashes every time I open it",
        "Won't open at all since the update",
        "Freezes on the payment screen",
        "It closes itself the moment I pick my address from the map",
        "app close by itself when I am ordering, very annoying",
        "reinstalled twice. same crash. phone is new.",
        "The map page is heavy and the app hangs there every single time",
        "Since the last update it throws me back to the home screen mid-order",
        "White screen on launch and nothing ever loads",
    ],
    "rude_driver": [
        "Driver was rude on the phone",
        "Captain refused to come up to the floor",
        "Unprofessional behaviour from the delivery guy",
        "He raised his voice at me because I asked where he had reached",
        "the captain hang up on me two times, this is not acceptable",
        "threw the bag at the door and left without a word",
        "Captain told me to come down. I have small kids, I can't leave them.",
        "Very disrespectful language and I would like this reported properly",
        "He argued with the compound security and then blamed me for it",
    ],
}

MIXED = {
    "driver_lost": [
        "الكابتن دار حول الحي ٢٠ دقيقه، the pin was in a totally different place",
        "الـ driver اتصل ثلاث مرات وكل مره اشرح له نفس الشي",
        "الـ location في التطبيق غلط، he went to the wrong compound",
        "الكابتن ضاع تماما وقال لي the map is wrong مو انا",
        "the pin مضبوط على العمارة بس هو راح لشارع ثاني كامل",
        "من يوم الـ update وانا اشرح لكل كابتن وين مدخل الحي",
        "الكابتن ارسل لي location حقه وانا اللي دليته على الطريق",
        "العنوان محفوظ عندي من سنه، والحين الـ app يوديه لحي ثاني",
        "الكابتن وصل عند الـ gate الغلط والامن ما عرف يدله",
        "تكفون صلحوا الـ map، الحي كامل يطلع عندكم غلط",
    ],
    "late": [
        "الطلب late وانتم ما ارسلتوا ولا notification",
        "صار لي ساعه ونص وانا اراقب الـ status وما تغير",
        "الـ delivery تأخر مره وما في اي update بالتطبيق",
        "كل ما افتح الـ tracking يزيد الـ ETA بدل ما ينقص",
        "سويت order الساعه ٨، والحين ١٠ ومحد كلمني",
        "الـ restaurant يقول الطلب جاهز وانتم تقولون في الطريق، مين اصدق؟",
        "still waiting، صار لي ساعتين ومحد رد من الـ support",
        "التطبيق يقول arriving soon من ساعه، وش يعني soon عندكم؟",
    ],
    "wrong_items": [
        "جاني order غلط مو حقي اصلا",
        "الـ items الناقصه هي الاغلى في الطلب طبعا",
        "الكابتن ناولني الكيس وطار، وما تأكد من الـ order number",
        "دفعت الـ invoice كامله ووصلني نصها",
        "كتبت no onion في الـ notes والطلب جا مليان بصل",
        "الـ sauce ما جا والكيس كان مفتوح من فوق",
        "طلبت طلبين ووصلني واحد، والـ app يقول delivered كامل",
        "wrong order تماما، حتى الـ receipt باسم واحد ثاني",
    ],
    "cold_food": [
        "الاكل وصل cold وانا ساكن على بعد ٥ دقايق من المطعم",
        "نص الـ order وصل فاتر والنص الثاني حار، ما ادري كيف",
        "الاكل بارد بسبب الـ delay، وهذي مو اول مره",
        "طلبت iced coffee ووصلني دافي بدون ثلج",
        "رميت الـ order كامل، ٩٠ ريال على الفاضي",
        "الاكل يوصل بارد كل ما يكون فيه اكثر من stop في الطريق",
        "everything cold، شكل الكابتن كان معه orders ثانيه قبلي",
        "الاكل بارد ومتكتل، والـ packaging مقلوب ونص الصحن مكبوب",
    ],
    "payment_failed": [
        "double charge على نفس الـ order وانا ضغطت مره وحده بس",
        "الشاشه تقول payment declined والبنك يقول تم الخصم",
        "الـ card ما قبلت ولا مره، وبعدها انخصم المبلغ كامل",
        "وصلني SMS من البنك بمبلغ اكبر من اللي في الـ app",
        "زودتوا رسوم service fee على الطلب وما احد نبهني",
        "الـ error code اللي يطلع لي مو مذكور في اي مكان بالتطبيق",
        "جربت بطاقه ثانيه ونفس الـ error، وانخصم من الاثنتين",
        "الـ wallet انخصم منه والطلب لين الحين يقول unpaid",
    ],
    "refund_delay": [
        "الـ refund ما وصل من عشر ايام",
        "وعدتوني بـ refund في الـ chat وطلع كلام فاضي",
        "الغيت الـ order قبل ما يطلع من المطعم، وللحين المبلغ معلق",
        "قلتوا 3 working days وانا الحين في اليوم ١٧ واعد",
        "الـ support يفتح لي ticket جديد كل مره بدل ما يكمل القديم",
        "المبلغ رجع ناقص ٢٠ ريال، وين راحت الـ difference؟",
        "طلبت refund من ثلاث اسابيع والحاله لين الحين pending",
        "رجعتوا المبلغ في الـ wallet وانا ابيه على البطاقه اللي دفعت فيها",
    ],
    "app_crash": [
        "الـ app يسكر عندي بس على الـ WiFi، وعلى الداتا يشتغل",
        "بعد الـ update الاخير صار يطلب مني login كل مره",
        "يعلق عند الـ payment screen وما يكمل",
        "اختيار العنوان من الـ map ياخذ دقيقه وبعدها يطلع لي error",
        "سويت uninstall و install ونفس الـ crash بالضبط",
        "يطلعني من الـ account تلقائي وانا في نص الطلب",
        "white screen عند الفتح وما يحمل شي",
        "الـ app ياكل البطاريه ويهنق كل ما افتح الـ map",
    ],
    "rude_driver": [
        "الكابتن كان rude من اول مكالمه وانا ما سويت شي",
        "الـ driver وقف عند البوابه ورفض يتقدم خطوه وحده",
        "تعامل unprofessional من المندوب",
        "سألته وين وصلت فقال لي بالحرف not my problem",
        "قفل الـ call ثلاث مرات وانا احاول اوصفله الطريق",
        "رمى الـ bag على الدرج وما دق الجرس اصلا",
        "طلبت منه يوصله للباب، قال لي that's not my job وسكر",
        "very disrespectful، ابي report على هذا الكابتن",
    ],
}
