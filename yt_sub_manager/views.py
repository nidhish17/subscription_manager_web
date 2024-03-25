from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test

from allauth.socialaccount.models import SocialToken
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from .forms import CategoryForm, ChannelCategoryForm
from .models import Category, User, Channel
from django.http import JsonResponse


import os
# Create your views here.

# test_data = [{'channel_name': 'ჩემი სუმოს ოჯახი', 'channel_url': 'https://www.youtube.com/channel/UCkMawSs7rSqGgiisq2uzGVA', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/KChPuSTj9OLIEpZOpPvVfH6WG-DNzers_jLH7m2Zmhk9CpPia2EusQjmK0qsHx421jcELJlRYQ=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/KChPuSTj9OLIEpZOpPvVfH6WG-DNzers_jLH7m2Zmhk9CpPia2EusQjmK0qsHx421jcELJlRYQ=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/KChPuSTj9OLIEpZOpPvVfH6WG-DNzers_jLH7m2Zmhk9CpPia2EusQjmK0qsHx421jcELJlRYQ=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'Harly', 'channel_url': 'https://www.youtube.com/channel/UCynuB1iXXgUf7MbDCCup45g', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/bTP-1HmOSDbH2dEmNPkava0FJxAel2lr67NCps3-AIRkaJAU2da68L2o0zh6vybt-92JQYHXjE8=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/bTP-1HmOSDbH2dEmNPkava0FJxAel2lr67NCps3-AIRkaJAU2da68L2o0zh6vybt-92JQYHXjE8=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/bTP-1HmOSDbH2dEmNPkava0FJxAel2lr67NCps3-AIRkaJAU2da68L2o0zh6vybt-92JQYHXjE8=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': '법공부하는 여자(a girl studying law)', 'channel_url': 'https://www.youtube.com/channel/UC-TLCIweHaMuuzXLubG5qjg', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/yF0ApjVI1ehZW_FqJW9ko4eOEapdxYC18GPbAWI5rtzH1Pgiszgh7wY4A-NjN-jwIVcyZsTm=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/yF0ApjVI1ehZW_FqJW9ko4eOEapdxYC18GPbAWI5rtzH1Pgiszgh7wY4A-NjN-jwIVcyZsTm=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/yF0ApjVI1ehZW_FqJW9ko4eOEapdxYC18GPbAWI5rtzH1Pgiszgh7wY4A-NjN-jwIVcyZsTm=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': "Rosso's Running Channel", 'channel_url': 'https://www.youtube.com/channel/UCIRhGas7Ac40F5wfi00GY-g', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYn92n4O3NuR2mXx-5TKqWxXgjtQ7120_7uAzE=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYn92n4O3NuR2mXx-5TKqWxXgjtQ7120_7uAzE=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYn92n4O3NuR2mXx-5TKqWxXgjtQ7120_7uAzE=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'Sumo stream 大相撲ライブ', 'channel_url': 'https://www.youtube.com/channel/UCeEHq0con4RRX6qLGTK1kVg', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/suBmuotTpr2JP--DLJqo38TiAFAW8ndaNnbV_34yarG69Cl-ixqnY5wY83lY9PV5iARY1Fsi=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/suBmuotTpr2JP--DLJqo38TiAFAW8ndaNnbV_34yarG69Cl-ixqnY5wY83lY9PV5iARY1Fsi=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/suBmuotTpr2JP--DLJqo38TiAFAW8ndaNnbV_34yarG69Cl-ixqnY5wY83lY9PV5iARY1Fsi=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': '二子山部屋 sumo food', 'channel_url': 'https://www.youtube.com/channel/UCq2bD4BLzP0hdtBw3c7BYEw', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/r42vpR-6dDaiy84BQieNn6cjwThAS3K5d3h65ykn77loomURWMtaS5KMnbVuRRdk1x6oCSgHP0c=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/r42vpR-6dDaiy84BQieNn6cjwThAS3K5d3h65ykn77loomURWMtaS5KMnbVuRRdk1x6oCSgHP0c=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/r42vpR-6dDaiy84BQieNn6cjwThAS3K5d3h65ykn77loomURWMtaS5KMnbVuRRdk1x6oCSgHP0c=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': "Runner's Digest", 'channel_url': 'https://www.youtube.com/channel/UCcf--bBI3oBTfcish9WACHQ', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/Wig143p1ftTy8d_gu_QywznAgJ4J36kOXIb3_-i6hNZHhtzmeOrwMU2nzMjvoqDuliMm4Th8RqM=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/Wig143p1ftTy8d_gu_QywznAgJ4J36kOXIb3_-i6hNZHhtzmeOrwMU2nzMjvoqDuliMm4Th8RqM=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/Wig143p1ftTy8d_gu_QywznAgJ4J36kOXIb3_-i6hNZHhtzmeOrwMU2nzMjvoqDuliMm4Th8RqM=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'Comedy Wala Kahani - Hindi Stories', 'channel_url': 'https://www.youtube.com/channel/UC2YjbW_Zz0Fl6LJBgN5ubcQ', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYpZhTyhcpkwOlCO_6bjRSbm8RdOsHX9uiYF_7TcQ=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYpZhTyhcpkwOlCO_6bjRSbm8RdOsHX9uiYF_7TcQ=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYpZhTyhcpkwOlCO_6bjRSbm8RdOsHX9uiYF_7TcQ=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'Jalsa Tv - Hindi Stories', 'channel_url': 'https://www.youtube.com/channel/UCHIYOs5N6C5AeIdWDxvrTgw', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/ytc/APkrFKb01PeB_CdISIpfXZIfGdM_hKKHamVGZ-PZLZ83=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/ytc/APkrFKb01PeB_CdISIpfXZIfGdM_hKKHamVGZ-PZLZ83=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/ytc/APkrFKb01PeB_CdISIpfXZIfGdM_hKKHamVGZ-PZLZ83=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'Virtual Running TV', 'channel_url': 'https://www.youtube.com/channel/UC-m-40G3vKvvxzJan9pX9kA', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/OLzJcQKIrlLfFDbCFOmFyKNHN_LagBdjp_Fy5O_HrhB2hgQG2w92kYG0_rUIUOr6pcCyVosBJg=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/OLzJcQKIrlLfFDbCFOmFyKNHN_LagBdjp_Fy5O_HrhB2hgQG2w92kYG0_rUIUOr6pcCyVosBJg=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/OLzJcQKIrlLfFDbCFOmFyKNHN_LagBdjp_Fy5O_HrhB2hgQG2w92kYG0_rUIUOr6pcCyVosBJg=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'Kirin Camp', 'channel_url': 'https://www.youtube.com/channel/UC4zNtKX3XTplYQWNFPorvXQ', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/9EDpxH8pkviv5sn2TD7_PdPXsyxixD32hVQOhsyBz9NOuTCi5gtnQ0lYIR1nlFIKr-Z4kPBUJA=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/9EDpxH8pkviv5sn2TD7_PdPXsyxixD32hVQOhsyBz9NOuTCi5gtnQ0lYIR1nlFIKr-Z4kPBUJA=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/9EDpxH8pkviv5sn2TD7_PdPXsyxixD32hVQOhsyBz9NOuTCi5gtnQ0lYIR1nlFIKr-Z4kPBUJA=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'Sumo Jason', 'channel_url': 'https://www.youtube.com/channel/UC6d4ZhHYVy3ANeBScnXML7A', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/Sn85_FG93Y3s7RHR974zdMvP9rQa62fv7i1nEeWCKdi0IH99zTjNfFytPHXTK8dnTVE-4dJu=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/Sn85_FG93Y3s7RHR974zdMvP9rQa62fv7i1nEeWCKdi0IH99zTjNfFytPHXTK8dnTVE-4dJu=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/Sn85_FG93Y3s7RHR974zdMvP9rQa62fv7i1nEeWCKdi0IH99zTjNfFytPHXTK8dnTVE-4dJu=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'Didac Ribot', 'channel_url': 'https://www.youtube.com/channel/UCsJJGg6hmHv2dCYity_PbUA', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYvA183xrojgseXXSWAz9yVgGq7pMe555fZw2Fsqw=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYvA183xrojgseXXSWAz9yVgGq7pMe555fZw2Fsqw=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYvA183xrojgseXXSWAz9yVgGq7pMe555fZw2Fsqw=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': '차밀린 Millin', 'channel_url': 'https://www.youtube.com/channel/UCk9P0tGC902e2jZRrTRt4Bg', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/6sxa1fO70kz250Wii0JvYUrc6qHspD99uhbX6GuAcvVQyZbKlutVSW9nlbweYsbMdtDpsLoLPg=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/6sxa1fO70kz250Wii0JvYUrc6qHspD99uhbX6GuAcvVQyZbKlutVSW9nlbweYsbMdtDpsLoLPg=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/6sxa1fO70kz250Wii0JvYUrc6qHspD99uhbX6GuAcvVQyZbKlutVSW9nlbweYsbMdtDpsLoLPg=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'BADMASH icON', 'channel_url': 'https://www.youtube.com/channel/UCRidj8Tvrnf5jeIwzFDj0FQ', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/ytc/APkrFKbtWP7C84vk1HNv2G2ncqcRAg4ibWE4R6LEb2UQkQ=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/ytc/APkrFKbtWP7C84vk1HNv2G2ncqcRAg4ibWE4R6LEb2UQkQ=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/ytc/APkrFKbtWP7C84vk1HNv2G2ncqcRAg4ibWE4R6LEb2UQkQ=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'Sumostew', 'channel_url': 'https://www.youtube.com/channel/UCClMvLPowPLwZ-YrYo4ybBw', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/ytc/APkrFKZgo5ZcS5O0Y4NxnJi46vmNIqwxNsbacI_m6uAM=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/ytc/APkrFKZgo5ZcS5O0Y4NxnJi46vmNIqwxNsbacI_m6uAM=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/ytc/APkrFKZgo5ZcS5O0Y4NxnJi46vmNIqwxNsbacI_m6uAM=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'YouTuber Shubham', 'channel_url': 'https://www.youtube.com/channel/UCi0uPoeyi6adI2Sb7u7rgdQ', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/tXEhR4Th24u-cgRV_UxgyGra1GJg9vZ2H9gO046BImerl0g8tBfJ3VsUnByJOZcgXtWiiIQMiXo=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/tXEhR4Th24u-cgRV_UxgyGra1GJg9vZ2H9gO046BImerl0g8tBfJ3VsUnByJOZcgXtWiiIQMiXo=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/tXEhR4Th24u-cgRV_UxgyGra1GJg9vZ2H9gO046BImerl0g8tBfJ3VsUnByJOZcgXtWiiIQMiXo=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'jaetokki', 'channel_url': 'https://www.youtube.com/channel/UClfCWq3PCqS2LdItAtGULFQ', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/fQCTsKaS1vSJGTGcdUGy-6fi_nKbSVxH3yG57qFNMiCe2njtTlIvIo_rm1zNVqrNxw6-u4QNiW0=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/fQCTsKaS1vSJGTGcdUGy-6fi_nKbSVxH3yG57qFNMiCe2njtTlIvIo_rm1zNVqrNxw6-u4QNiW0=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/fQCTsKaS1vSJGTGcdUGy-6fi_nKbSVxH3yG57qFNMiCe2njtTlIvIo_rm1zNVqrNxw6-u4QNiW0=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'Tech With Tim', 'channel_url': 'https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYHht64W4oJH1AaeZH7o5CBS2B2xLMTDrPyaN0TiA=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYHht64W4oJH1AaeZH7o5CBS2B2xLMTDrPyaN0TiA=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYHht64W4oJH1AaeZH7o5CBS2B2xLMTDrPyaN0TiA=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'Misti Tv Hindi Stories', 'channel_url': 'https://www.youtube.com/channel/UCjgiEGaXfuQaI7xdDSXRZ6A', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/oqpnTU4in5vbDp5ia65kivyRluGqg5BGRwfG4NQVVD4bGllgEjmgMnKKUlq-B1Thkwu8HpbyKA=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/oqpnTU4in5vbDp5ia65kivyRluGqg5BGRwfG4NQVVD4bGllgEjmgMnKKUlq-B1Thkwu8HpbyKA=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/oqpnTU4in5vbDp5ia65kivyRluGqg5BGRwfG4NQVVD4bGllgEjmgMnKKUlq-B1Thkwu8HpbyKA=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'SUMO PRIME TIME', 'channel_url': 'https://www.youtube.com/channel/UCLtOECZPTHBnR6X6Vg06LDQ', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/_iyrzEn_zZ5-m8Fk_voErQ0PLV3te6ZbNmia9BYofcqZJLROo51f0hL4tS1_osg43tuHovRbIg=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/_iyrzEn_zZ5-m8Fk_voErQ0PLV3te6ZbNmia9BYofcqZJLROo51f0hL4tS1_osg43tuHovRbIg=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/_iyrzEn_zZ5-m8Fk_voErQ0PLV3te6ZbNmia9BYofcqZJLROo51f0hL4tS1_osg43tuHovRbIg=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'Scooby TV - Hindi Comedy', 'channel_url': 'https://www.youtube.com/channel/UCdnOG_jDq5TR5sWuQkoZHMg', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/gdkiwvyzwrkY1iRcNb5cW3GOVGe3f5L8M49gPHOJj3oamwfrIQ5mWUlusBjGJ1tiHFSNlHzb=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/gdkiwvyzwrkY1iRcNb5cW3GOVGe3f5L8M49gPHOJj3oamwfrIQ5mWUlusBjGJ1tiHFSNlHzb=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/gdkiwvyzwrkY1iRcNb5cW3GOVGe3f5L8M49gPHOJj3oamwfrIQ5mWUlusBjGJ1tiHFSNlHzb=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'Trilogy Media', 'channel_url': 'https://www.youtube.com/channel/UCca2961Ton2js_f9IDXK9Wg', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/23zNsrLLY8lQFbZhdFbtvN1N45Wuc5CgWgmYMddoAX6jI4kxky1JpQ-ekykVM8n82uWUNffc=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/23zNsrLLY8lQFbZhdFbtvN1N45Wuc5CgWgmYMddoAX6jI4kxky1JpQ-ekykVM8n82uWUNffc=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/23zNsrLLY8lQFbZhdFbtvN1N45Wuc5CgWgmYMddoAX6jI4kxky1JpQ-ekykVM8n82uWUNffc=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'Fireship', 'channel_url': 'https://www.youtube.com/channel/UCsBjURrPoezykLs9EqgamOA', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/ytc/APkrFKb--NH6RwAGHYsD3KfxX-SAgWgIHrjR5E4Jb5SDSQ=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/ytc/APkrFKb--NH6RwAGHYsD3KfxX-SAgWgIHrjR5E4Jb5SDSQ=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/ytc/APkrFKb--NH6RwAGHYsD3KfxX-SAgWgIHrjR5E4Jb5SDSQ=s800-c-k-c0x00ffffff-no-rj'}}}, {'channel_name': 'MR. INDIAN HACKER', 'channel_url': 'https://www.youtube.com/channel/UCSiDGb0MnHFGjs4E2WKvShw', 'channel_prof_pic': {'default': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYuSw_UwxtuE0lTvA2--cixKCKbsKKQXxqmTRVwsQ=s88-c-k-c0x00ffffff-no-rj'}, 'medium': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYuSw_UwxtuE0lTvA2--cixKCKbsKKQXxqmTRVwsQ=s240-c-k-c0x00ffffff-no-rj'}, 'high': {'url': 'https://yt3.ggpht.com/ytc/APkrFKYuSw_UwxtuE0lTvA2--cixKCKbsKKQXxqmTRVwsQ=s800-c-k-c0x00ffffff-no-rj'}}}]

def is_authenticated_user(user):
    return user.is_authenticated

@user_passes_test(is_authenticated_user, login_url= "login/")
def home(request):
    category_form = CategoryForm()
    channel_form = ChannelCategoryForm(user=request.user)

    categories_items, channels_in_category = get_categories_and_channels_in_category(request).values()

    # for passing the received pagination token to the google api function to retrieve the channels
    page_token = request.GET.get("page_token") or None
    # call the google api function
    subscription_data = all_subscription_list(request, page_token)

    # retrieving all the necessary data from the subscription_data
    subscriptions = subscription_data["subscriptions"]
    pagination_token = subscription_data["pagination_token"]
    prev_pagination_token = subscription_data["prev_page_token"]

    context = {
        "subscriptions": subscriptions,
        "category_form": category_form,
        "categories": categories_items,
        "channel_form": channel_form,
        "channel_model": channels_in_category,
        "pagination_token":pagination_token,
        "prev_pagination_token": prev_pagination_token
    }

    if request.htmx:
        return render(request, "subscription_component.html", context=context)

    return render(request, "home.html", context=context)



def get_categories_and_channels_in_category(request):
    '''
    this function returns all the categories the user created and the channels the user added to the category
    '''
    user = User.objects.get(username= request.user)
    categories = user.categories.all()

    # get channels in category
    channels_in_category = user.channel_user.all()

    return {"categories":categories, "category_channels":channels_in_category}


def login_page(request):
    if request.user.is_authenticated:
        return redirect("homepage")
    else:
        return render(request, "login_page.html")

def logout_user(request):
    logout(request)
    return redirect("/")

def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_form = form.save(commit= False)
            category_form.user_profile = request.user
            category_form.save()
            return redirect("homepage")
    return redirect("homepage")

def populate_categories(request):
    if request.method == "POST":
        category_id = request.POST.get('category')
        channel_name = request.POST.get('channel_name')
        channel_url = request.POST.get('channel_url')
        pic_url = request.POST.get('channel_pic')
        user = request.user

        category = Category.objects.get(id=category_id)
        channel = Channel(category= category, channel_name=channel_name, channel_url=channel_url, pic_url=pic_url, user=user)
        channel.save()
        # print(channel_name, channel_url, pic_url, category)
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "not a POST request"})



def delete_channel(request, id):
    channel_id = Channel.objects.get(id=id)
    channel_id.delete()
    return JsonResponse({"status": "success"})

def delete_category(request, id):
    category_id = Category.objects.get(id=id)
    category_id.delete()
    return redirect("homepage")

def get_credentials(request):
    access_token = SocialToken.objects.get(account__user=request.user, account__provider="google")
    credentials = Credentials(
        token= access_token.token,
        refresh_token= access_token.token_secret,
        token_uri= 'https://oauth2.googleapis.com/token',
        client_id= os.environ.get("CLIENT_ID"),  # app.client_id,
        client_secret= os.environ.get("CLIENT_SECRET"),  # app.secret,
        scopes=['https://www.googleapis.com/auth/youtube.readonly']
    )
    return credentials

def get_subscriptions(credentials, pagination_token):
    youtube = build("youtube", "v3", credentials=credentials)
    next_page_token = pagination_token
    prev_page_token = None
    # running through a while loop to retrive all the subscriptions
    # todo: add an load more option to get more subscriptions instead of running while loop

    response = youtube.subscriptions().list(
                part='snippet',
                mine=True,
                maxResults=50,
                pageToken=next_page_token,
    ).execute()

    #retrieve the subscriptions if none then just return []
    subscriptions = response.get('items', [])

    #get the next page token
    next_page_token = response.get('nextPageToken')
    prev_page_token = response.get('prevPageToken')
    # print(prev_page_token, "prev page token")
    # print(len(subscriptions), "len_subscriptions")


    # print(next_page_token, "next page token")

    return {"subscriptions":subscriptions, "pagination_token":next_page_token, "prev_page_token":prev_page_token}

def all_subscription_list(request, next_pg_token=None):
    credentials = get_credentials(request)
    subscriptions, pagination_token, prev_page_token = get_subscriptions(credentials, next_pg_token).values()

    user = User.objects.get(username=request.user)
    yt_channels_in_category = [i.channel_name for i in user.channel_user.all()]

    subscribed_channels = []

    # print(subscriptions)

    for channel in subscriptions:
        title = channel["snippet"]["title"]
        channel_id = channel["snippet"]["resourceId"]["channelId"]
        channel_link = f'https://www.youtube.com/channel/{channel_id}'
        if title not in yt_channels_in_category:
            subscribed_channels.append({
                "channel_name":title,
                "channel_url":channel_link,
                "channel_prof_pic":channel["snippet"]["thumbnails"],
                "channel_id":channel_id
            })
    return {"subscriptions":subscribed_channels, "pagination_token":pagination_token, "prev_page_token":prev_page_token}
