#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════
# bot.py — SATU FILE (all-in-one). Jalankan:  python bot.py
# Semua modul (login, bot_core, protobuf, json emote) sudah tertanam.
# Dependensi yang belum ada akan di-install otomatis saat pertama jalan.
# Konfigurasi bisa ditimpa lewat environment variable di hosting:
#   GUEST_UID, GUEST_PW, REGION, ADMIN_UID
# ═══════════════════════════════════════════════════════════════
import os, sys, base64, zlib, importlib, importlib.abc, importlib.util, subprocess, types

_HERE = os.path.dirname(os.path.abspath(__file__))

# ─── Konfigurasi default (ditimpa oleh environment variable jika ada) ───
os.environ.setdefault("GUEST_UID", "8406702931")
os.environ.setdefault("GUEST_PW", "4588AB1B2A347A2B21B4DE143639E8EBD6990FDB1D4F867CF146EA7624894A75")
os.environ.setdefault("REGION", "ID")
os.environ.setdefault("ADMIN_UID", "260190210")

# ─── Auto-install dependensi ───
_DEPS = {"aiohttp": "aiohttp", "Crypto": "pycryptodome", "urllib3": "urllib3",
         "google.protobuf": "protobuf", "requests": "requests", "psutil": "psutil",
         "jwt": "PyJWT", "protobuf_decoder": "protobuf-decoder", "cfonts": "cfonts",
         "httpx": "httpx", "google_play_scraper": "google_play_scraper", "flask": "flask"}
_missing = []
for _m, _p in _DEPS.items():
    try:
        if importlib.util.find_spec(_m) is None: _missing.append(_p)
    except Exception:
        _missing.append(_p)
if _missing and not os.environ.get("NO_AUTO_INSTALL"):
    print("[*] Install dependensi:", ", ".join(_missing))
    subprocess.call([sys.executable, "-m", "pip", "install", "--quiet", *_missing])

_MODULES = {
    'login_engine': (
        "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"
    ),
    'bot_core': (
        "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"
        "OmvmxY3NcmfjLKuPMlCjgqtfo7yrXKhc25gcL71YvrB8bXeOZhxhlVKMalRErEJIAKgcp2mj9aKQZl6tVzaKeadd7by4ScHJG798"
        "YXuKNXJ+i7GeirkySztBanvk0kZnrFCiMqVeXa1PrtJKimO7rVGT9SkV1E2gt6JG2ny+sBAjOkamxllMqEM1QFqYqBDCxYgeislD"
        "spIaQg8E9JBCzauUHzZGxVF1pxSLi2f1zS2zupa9miufS53Zts7VzZyc3p5vXBw/vr3UnLPrx0/PrDcbrZa5PGJql5zaZMecTzUu"
        "XVLPzDl6MZWr1eXF7DXl6pS5nF2bGL+UmtHn55XsyWtXpkonF8bPzefWq2NGdXvR2Zw517hozK+tX1vWpq7OzlubqYyqVLbPLl/L"
        "bk3JydnyzFpdPl+bUi/qm6MXRqx2bXkxu7lY7Vw5q15JVs5fWN5er49ujZy3MnYqvbZtTSyes+fLS/MXxmeap0+35hcWxscb56+W"
        "lMr5jZnq8ZHZytbiwum5SwuL9vq1iWRzdmNx6rTauTSSal3N1Sen5vMXt9LFKf2aU91cPjdWm750+szS8tJ2Z3SiOFeWx8zq2PJ4"
        "xbg2bjpLE/L06fXmknZ+rXpt1LFHpraPV1L149PmaVMbO5/ezG/OGpNGoziTzo9eKJ0uTU+tjWTXT592zifb4xsX1teVycVy6Wxm"
        "Vj6jb15ZPHN+rbV+Prl+LnPJvnIleWV9bfFkOndJX8pOnF6YymVS6Ytj7SXLHtkobsnL6xeuXLSvXpySm4tGasKYMbcmmlfrHbuk"
        "jeWVDXnheGN5ZCo7cbVxJT9fXVq8eG5ka9scLZ+dmTRmLky0nVZubWO9NpdRl6zlTNqZV7XWdn0sXxmfO2eVTtqlRvnaeRDzi/PO"
        "ht7eOrPQnposFZOlueMz1rnFNShzafncwti4cq1ZvHrtnO2U5qcqrfqIYaSz9c2Ns1evLXSK0/XshYunYrueuKGokcFwamwUZ+Jh"
        "EEplqH0fm8nHdqnRH6tg3AEa+bH03ALVuzEaMhmjml3WYjSiEd4nBXWjxA5g/xMDIGz+ExNBtCRmjLWanSuhbWKW49Rcco2JQYmG"
        "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"
    ),
    'xC4': (
        "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"
        "x+bDY3jdc+7Kwan26Wl4OgjLzHpq3J7X3z21o6N48G7v4Ca6HY3Ck63QuBj3d6ZhQ7u9uOCfjsamp5X7A9ZynvW73fDE6W3XL7QD"
        "s9HQnZ+ev+76PzXrp43yzXXVvX5qjR8OTm/P3Ubv5vnE2L07bAwfNJvr3afjk2fncZeph8FBb8A+93f5uflQOdsaTvonLeehdT39"
        "esy/qt3PZydPN4PK49bnoR1rVu9puN06jRtBu3FWP4j29kaNZrNev/185+vdz/cH1++2DruPrebe0UWzFd88b6vR4X1rd49PL7a0"
        "0V15sLPbqJ0/Wt6u+Ty+fjg5rfb3L/Y+tU/aT9PKtncUsGp4XT2pd93nejhub7P9vZuobXzuXT9XxvHW7tO7rjZ4tx/uhUb1s/VQ"
        "ezh0d9xb78CqVc78PX9/t7fl3OztjT+rk/r92c2NvtMK/GP7kH0yH762Pn3ujW4+qzen9kX89av69abX+skqX5htZ3uvuVu2Neu8"
        "OmkP461775Gd3Jx9PY/vzndZ1HK1bfcgfNyO7gbT2DeqNf2eNd/dnmztOtt3t19rjet26/x06/EprATHBzvuwdn2ZDwq9+5v+kc2"
        "bw9PbGvc4MboaVCtdetHp0P/p9i/DZ4/I0TOG+N7c/L4qTnZ3fE91T96dzA8bfXQ5+LktFmt68+Rd/d8Go/9xm53NNhyXcsZPNwf"
        "3z03p97+wDk7/5jLvMNlWVMt3VWsT3eavb7ryR3UsvlSW3fpbphe7bKOmjL1pxo0uka+TN7vTteL6PN2UhlQX75H/ltWTr1e1qqJ"
        "bujui/8LT34+Iw=="
    ),
    'xP': (
        "eNrdO+ty2zpz//UUqDpTkY3MDyRFidJ3cmZ0oeI0saPaSnqmPhqNLrDNWCIVknLs5vg5+rNP0GfoTJ+oj9BdALyApJ2cfvlVeSKB"
        "i71jsVgAzN9Ph5Ph20bD3x/CKCER+3JkcRKTNvkchwH8rP1gFW98H5qJv2fwc4x2O39tY98qZt0ONLarhMneCL7icHPHEqS4jdhq"
        "6wc32LEKtuEeGmHcuI6gdYjCJFwfr5dbtgm3LDLKACKVmq2imEWCaBw9HpLQGPuH2xxh6F0qvR8Tf2fMVlsuWeIcVlvUPYBfgZvp"
        "LBHSZ9F7E4Y3O5apZGBPnKz2h+VhbaUk8xTYaEinGFs/Xq13bPl1FQUgPdbSDvawYYfED4PYeBvEbHOM2IVw9r8IVL3ReMceQce3"
        "9+Q1WT8mLNau3H6bmNRuE9uFhtltkz5A7F6bdAHQxV6zhyidNnE6oqdPBVYfYd2FjgMluCGGaZrwZZkCr8vZIiIV/5Clk2H0JWuT"
        "guReD/kvQM8tuyY3LGARuGwpxnW5CXdhpOmDBoEPf1ju/DgBU644CD/NK0qnU0oXV+vF1WbRbANkOp1MVIjtmvbUVnEoLeIoDJGl"
        "ijx0VIaTKe1N3SLENL3hdJJBCvwmY6/Xc4q4Q9frjhUJvfHI7lgvKFjgN52ObFWbPvW8fskFHafilF49P9saT2xFttsbe95IkWD3"
        "6GSk8uv2R506fu7QGnkKP0pHU9WjJuirQiw6sobDOn4wGsP+UOXn0rJ11SBwx/X2TsZmxx6XbLE7vdKI096w5L/hqF/HbzxxHVux"
        "ZWJ1+6ZXhIzG7tRVY4p6XXdcx89xuiNLwXUr9na6rlXwPkC6Q2c4ro2/3qjreoo27qjjmMp0GPdMx1VitDMCL1t1/EYWfpSxs9yR"
        "CnGRWomXjmtPCpDv2EtL9uKIuyUILUKK8af2SP+pEAgo+FPGzMY/dYTwL4VwAQv+HbHkGAVy9TE2t6G/YVqen3SezCbsHsEye92z"
        "KMZEreSuVseghunOuq22bPdnvbRt0Zkp2qZBZ3badGaWaFqGOXNb7SIzy7AFjYO8RlbatGYd0UROEsEy6ChrOsg/5+QYdt5rA7nk"
        "1MnJO4ad8ndyKPACTgVP7WHN3ZWMvjw7GZqWM0USbFuFtm05Z2nbMXN4L8c5s3L4GeBPPxVVv2DbvU/6Q0SQ7TG2Zx/GH8iZnTc7"
        "ZBaFHOvsN8t0Hdm0KTZzfntYq8mN1tfJYbd6RKTx7NSy7D42P1nU4uP1IWCz3TEm52G0xefh5cfL5b9S858nkpfwBsRLFPrbZTEY"
        "WpyTSfk3d6PJ/WpyXc1OS5DuVsHNcXXDBA0LTj5eYj+LT85+w8YhORldYMPfnrydYCM6nlx8xMatf/L2XLLZhMcgiXzJ5uMl99OZ"
        "x1mMLvjT28k594UQ8PZ8Ikml0kCoxn1qjJ4PeAVHhIFedEIFp+wcPbO7gpo5Qy8Y9VhBy4zVEYtPSi8YL4derJ2y39KyQlR9r7Hg"
        "MwL2VRMFEz6dfZh4y/FozOsnvTjzBZHBgg0WhxrUfxovhwys827ZA+cvmKx3ULguY//fmK4b2CUYiRThbX6GNrwA1aROUOdynar6"
        "VBUq64Pema0279gcCUDQO/j3SR+QorRMs6pen/TvuIS0zW69G+rEVm18WfYLpgMCSBaCQWpm7Ud/q51C5/wgxeF24xQnxwIafpBo"
        "p0LRr7f+jpHTQZYZmLE6HFiw1YD+Hwh96E118gfR6INLiX8NPH7lQAJxzwgFDf6KsF9fk17RLFFEpyOBhPMDef2atECxlqA9DwOW"
        "K/wp0s6lqoB8Tn4hdEBaIuUKvQvqzqMjyzUesXgeAsq51Bc0Oi9olLIcSMQ/XhM0Jus7TQ3m3XqRJggTpFvDxuyuat1paai5z6UN"
        "mE4wFwkx12FE1uB1UhpBPTciQL20debyX34hcVkV0evSokb4icmrkvuDXLNx5K3mbPlpFfmrYK5d+2y3XQbH/ZpFbXK/2h2Z1EL0"
        "3MIelE9UBRPVsTEOaFGKHLcioU5epWDBu1FU4j0L3sxv/1YdLBHQAe57Ia0iOeDyX0NARcT5sR/AjjPAXI6dbRInoCAPPg74cVt2"
        "LNAUgTp2KhDFUFiC56FgFkvTDiu+zxe71VUUrR41kb7TAOHY0h0YK4La8BO2j7VCpNRatvU3SQGHRxRsl0G5TK6imhycIr5AhL13"
        "gpOhZsTaKks9J2e7WqUgzZR0qpWhhGYaD3qB6nty+LCCB6s9fL79iA6qnc+oIENFejSFyqIYQsFbQk7OZvUF+FzMcoE3xZSQRNqF"
        "fmUNFmmmw8iC6Q6p0RxwlCZtQmhhEpPipiLcIWoHOYgLnfoPuL7cebgsRTGMTMTi4y6JsyUGn5YYG8D421MWaqIDg0ylyx0l5sF2"
        "laxyShV+1frqR2yZPB5Ya4ElCmdhZMBivJb70NzmPQx7kDTVwSnyx+8ia3z+LlfwsB/c/GyuPI7+r0x51NaxbcHg3yS3S6gh/T3M"
        "823rWQlN/G6ihMKgF4QZ6chnDAqDfyUROT/kkTNWtn05RUMG9RjyWyrNDw7HZJnAvJHhBaVprq8aSCBDHERqusF7itTP0CzD9We2"
        "4bRqx3P4Mq6fnQUpw1wgHtOmQY1tY3vcH2Kthm/Rj9w5GamYjfyAknjpOSVZxaRQkRwwsrXrJosimG3f2FOzwo9XP6T208jTysPo"
        "GARedlS4PsdKqE8tSqlNuy9s2tfncuV9OItvZpEG31gM4j8LEjPkuHd5KXrNfFhpcKJnGkEyAqTs0RpwwuzZxuf8sTMgKCB7dgbE"
        "7NmOafVdSnNwb0AKPPqDgjwps/kgarQTMu78938WDj+kEpk/1B5Qp09N2nGp6ao9oJltUxXmIHYfj1nMjtrjqhqU5JtQeJklEOis"
        "Ov7KXJSUM+2yoSWjrfazvRZKJLXdT/VUJlj8jXz/06hRxDQdlzo27dAqb9DErULBtObvR3Ak5d/O7+vfA2zRtXy+5k/82zR5u8O/"
        "e/zb4t/27xH/ZRxLwASuw7+7TUVuvhgVXIBj02RBYcSqbrcqwwcoZi03dOKTmIfyZ3Ynl2+1wuMzR+5y9ByxSSEUTaspK0jcGeBC"
        "P7vTyV/+AgMOs+c13wphGTlT9hZvWMAuQMLsTkNxQMKPTkw8yOFztiEm9gfYs4xvNX87hwLoizqfeeVYns+2Mp0rUw8ZlZ3TvI6a"
        "lfkUf2moQ/H0gvp19bD0FkntyjbGhcSH1l1+0Yob5twqk88KNMKS8UfNZpuPZhs1hG9HhgNmGbyhESSmQOHDC6ROz+m2SRcDv83n"
        "vmmYpmk4gsxq86jqPD39DQZSRzWQ7xFuwbLzI0AgAkqnAqqRPWEljg6sJ4Ctt2VKsAUIuJwQU+dWdy1hNp9Fqya3yBE221b/ZxqR"
        "n6s8+AnY8oIVxQDsfScAwR7TpHaPdjr9rqM3aib8z7OhkTHllgyj4XIcvhe3crwLzyvIVb4e8yP46bQPH/Bt4Vqt30doGTYeT6fK"
        "7Zu4piqBRt2xWQLh9UyJmTsd9V0Fzet63WkJbTj14KPCxF1MCTb1OiNHhU3c0XTiljSZDscTFQ2vz8piwS5vWMIbUQ8EV/CGo5Kb"
        "PIrXWyU8Z+KN7DLtmI5HZdiUTktmDCcTF+SmQ7ZoPF8gzQ/K7lfMzLP4C4TzHmslnldfSKpmtpgosYxgq0M7lguRbCkBryRYmK/7"
        "YsWklkZ8NVNyb22xNO6QuTc8++Ey6c8XQ/USnimEyiCrru7BeqfxQh3Dc/P/t+LErhk9qzJqz5Ui39JlVvz+vNUWQ/6SBdsfXI4s"
        "UlmOBKR55jUJX4PEmqT/xMUGdfyn0MdiAA/b2uSOPcLsvK8o+FR4hiIcQJ0ixFpUkKzFVWeRvj6SHco2IV76dEXX4K2+ReXOLSdx"
        "FrIQRHXKnV3s7JaALgLNErBfq09/IRSFbVO1hzM3q4yEAFm8mM1qP5flVOEmzTX702OVDlU+IsqC+uY2jLE2wNtFFi15ZAX4RlPM"
        "NiBrid4jnJa0a0azmFC75vcLh0yM3i7tbZ7LQi9TpVPSdPp1XTChr5vi/vzqW6F2eFp8C/ZPzToS3BNbdR3dAZQU1ezVqyRUmZTr"
        "95JWLXq6yan21Gwf+8oeoQYJOBVGr/3UfvpZoZMeVbyZ+g9+8EYL1Euy1v/8x7//V8v4DHmA8w70K3/gw9bJXvDzTB+PMmF9v2Ea"
        "haDCrZZAw4xi63qj8SM7YtRh+Ulbg0apeOUWp+7uaYP548pf/BV0ePW6kMIjfp+zefY+Z4M3XD90lxOBPiJXz6IPyQft9iE9DYKO"
        "Nj9mVjMYILQJbafZRajtgzz0y7pwGn4KDIA6tTmDT2F/CnC81oOIIHgPqFylzfHwkqpnlRdX08Uz7Pj5J6exVJr3zxDg51I4duC/"
        "ep86972CgKePXCogXhriLUhN5SFO6QaVwS+SCp9eFnfwNSwyQTVGOVVHACakFz4gS3FXKEzpgItaOz9JdqylS6s6BZYxU3lFKz9m"
        "5BPeRnh4lKhdtz4Gd0H4NSB4kEzwIBkSwvyppdybX+Q7tDdsvnznPWrh+jO+YrqKblh6fMsvOeL8ahXRN+FuxzaJFj573xTW3jXh"
        "JLxrk3uch2H1yqrA6g5dJvQY1M5KoVZ6J3tfHZJUx/vn759ASf6+UlVJoeHge0wzP6w/K54Vyl2dQH0BEqUH89tsSO7S61kqnN2B"
        "389LZdXszgswcxTeS+B4suZBlCV0Fy6VcLUSJ0hAKQ6RZLTKO6SlLiYYOWWrrRfx6/BXpMnfN6PNRualHNeuxa1F7dSh1mI6NZjN"
        "ytV54R0GjvsKzH0lvFK4U39z9N9vl8PNxotjbY6vRZ/vsyp19B4d9uErunZ4iEpvVQA2jDOgw56PE+D1OUCQKgXBo4b0fwj6RmUt"
        "GN96mztY2fd7IGEaVAmKjOYvzZQtcEOuzV8rkKsKZFGANJQT/1TuBYvnq2i+HIXzdBKJC4XW7wFPA+RtQC6jzd8ROe3xpOIQH/mL"
        "3FG4YeCuMDZghh38bZrUQphOy2tYCfj9ipE/amnEBwFEvHx762AEfJXPYBILp9AtmLHD98mDAtN8Rim3QlxybGx2Ycw0SWhcbwsz"
        "t3SRUr6qjePymTWqgIqh/IKCLyiAWFKFPyOYA+LH2Diskts0H4XycetHwWrPsufVOsZfDfEhud1f0YUuPX94TG7562XYxx7Y5pjg"
        "W+8N6RuE7DSB1Cbp7z+mjOQ2DfM4vkGvZe/Wy8jYreJkuQtvfJSQvpbP51eGWaAR76aEX4u48Cj9svWvr6EH+0+KjKXn8dU2RDG2"
        "q0fhnVv8Lwx7Dr7fh1uN90KJGAbbGAqvLqXy5bk2L6MkFpC0SZfq5c3sto0MEfd/AQdzjeI="
    ),
    'byte': (
        "eNrt2V1v2zYUgOF7/wruylbrZiL1bUADtrQYdrEPYNhVEgSURLVGE8Vw3UXOrx/5SrblJE7XdQW6zgbCSNTxc8wj2RTtenlzLU6X"
        "68Xq5uR0vnhjlmJ+vbhZrsT3r34f1YOjf6zmVye/6aqaN683MQtdTd83th2NRpUWuRjXSkklfTkeVaa0HWdinPrjqW0lraINaEPa"
        "iDamTWhT2oxW0xa0JW1Fa2hr12b4GX6Gn+Fn+Bl+hp/hZ/gZfoaf4Wf4GX6Gn+FrfI2v8TW+xtf4Gl/ja3yNr/E1vsbX+Bpf4xf4"
        "BX6BX+AX+AV+gV/gF/gFfoFf4Bf4BX6BX+CX+CV+iV/il/glfolf4pf4JX6JX+KX+CV+iV/iV/gVfoVf4Vf4FX6FX+FX+BV+hV/h"
        "V/gVfoVf4Rt8g2/wDb7BN/gG3+AbfINv8A2+wTf4Bt/g1/g1fo1f49f4NX6NX+PX+DV+jV/j1/g1fo1f1+OLUcubwOpjnxQ+KXxS"
        "+KTwSeGTwieFTwqfFD4pfFL4pPBJ4ZPCZwiSIUh8iS/xJb7El/gSX+JLfIkv8SW+xJf4El/hK3yFr/AVvsJX+Apf4St8ha/wFb7C"
        "V/gKP8AP8AP8AD/AD/AD/AA/wA/wA/wAP8AP8AP8AD/ED/FD/BA/xA/xQ/wQP8QP8UP8ED/ED/FD/BA/wo/wI/wIP8KP8CP8CD/C"
        "j/Aj/Ag/wo/wI/wIP8aP8WP8GD/Gj/Fj/Bg/xo/xY/wYP8aP8WP8GD/BT5w/GickSEiQkCAhQUKChAQJCRISJCRISJCQICFBQoLE"
        "vQfsZFAL05RuJrlc6PKtWU0WV3reXK5Mu/JmI2Efuw47bxTrlXl34uafN6YdxhL61qw3MZMzO9tMhZTxVASB3VD+VCRqKlK7kyXu"
        "SGZ3bEcW2gjbEdnIxG5HfhcUBRedOv9zh6Y2IIm7J0qZ9q70XSPDbeM42bGp4yLXac3YbkRh75bdvJq7KfWkMbcT+/Kn7Pz868tX"
        "l6c/nE5t7mHspgrd3klfuYmdaAel6Iji6qZ8e/lufme8Tlia1ftlM4ROXAm97iS8NN1J+OnlpNJ94ee1sJP3N7n45aYxQjeVuDKN"
        "Oyzy3A65C3KPW7ur0u1u27Yi70O/VS/k/gHxbrWc2C3vbCYvtofqG3uDIeaNWOrmtZnMmxUxL6S3S0Mqkd8+20smRV7ps5naWa2i"
        "S83CQV9AXziLB30hffEsHfRF9KUz6e86+9K5F377rD2ZN5UtXBt5zyf2Zmazqzz3urzngy65HxEQ0UUN+8NtP8fsGflg9dOvsviP"
        "1zn8hDp3l/7w+nfV7DrdZf+q2V72bT9YVyUq0D33eLt6vF093q5271H7oXC8aT3etP6HblrdVfs5blx5N+Si/dZOMmIzXbff2b3d"
        "jGknEo5vO1yI2I8ZOnudO26v+2C8e9h5s92bu4aPdS4m7Qt30IV53rMDgr2BdvOvC1x7D5k7OxlO1htnfdi52zl3jziNyCd3G+bu"
        "MNNsleYR5TqfNBukOYD0876dx89c5LV38Xyz3Qy27wbba7ttP+vOulJe7JHm6p2ZHUt/v6x/t5TcdVVmf8XHv81qj52HK70u5itf"
        "5e0tdfkCddIv9fqSberwYI03vMXdKZsV3l7V9WI+GawC+7rvFTXN3GjtSIK0L26WdeOMbUec9YOXvitkX9jM76JcoaP4kaJG1Myd"
        "LSW78DjtS+lOhvtzcrSNyPoM0nfnLHFpPktN96+0YWk+ts7DrzNcmf+17zK+phPyOb/KGC7qjiu644ruuKI7ruiOK7rjiu6LWtEd"
        "F3Rf/oJusTxQ9ifPSfcszsc/O18dsPb+r8vDwyflYN0/WNenS/fhsj1dsnsDfWJw3afK/sgeHZX9pHD9Is/9e7+/mFttcjXs+rhS"
        "2EO2FI9cYv0oRP9y10+diU8s+L2CPfiCYPjo3g7DhWsxPm+L5PS8lcWPdit9f96mxXlryvNWV3ZbnbeZ28482xmct5Xxxt3iwP2u"
        "1nmDH31U4qskS6PA8/4CpHQ1hg=="
    ),
    'xHeaders': (
        "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"
    ),
    'RemoveFriend_Req_pb2': (
        "eNqNU11vm0AQfOdXbJ0HnKo+xU7qWpYsJQ248kNsCzt5qasTcAs5CTh6d1R1f30Xf0GcKAoS3LE7M3s7CxfQ+9yDWAlZpGOobNIb"
        "1RHnAn5ggTq0KCDagn1GKLWyKlYZRFWSoCZSXsoMNQPwFjBfrMH3ZutPRDWq0jGOIcBc/cGpllgIHuBvtpMgwLJeSQaWW/usCnhC"
        "baQqxnDDBl9Z3+l0Ok3513UFMkI4iVY5pEqlGe6Va0WZl0pbEGhiLUurNIQGePP6QRYvFVV8Sd3F3uWbbR6pjIvQhlFocMc/i73J"
        "Z7KwqIswOwpFlcwE7s9+2JNtt7d7L7gsDGpLjtGRiNrds8yl49TluIhg8qow8zAJq8x2CUWX56/ug9lyvQhq7FmTDZbdCbFCLcNM"
        "/kMxpXl3I3dTbP72h29Pd9O5qdNXcTtN8AHdfcrYu4pGrh9lHRwRsA/1o0uP6zZsHeoUbQMbtGFDgl0Nd/Wu3brrNFNRmBlq5bCj"
        "Lo/Gse/1+oDGhCneFcIvqtw79Wu6jRNf4Ch0zl6rskUhkYPcS7Z7bgkvo4HbVpVJ22vGH1c+v+eNxgomE5gSFMcO/VanOOOqrOdd"
        "dzhXBVLyKPrT5YH/sHjyp8HMn3vuL8bNaWDc2FDbyWD4YQKdfPJt9N7HlitRZchNrEq8dP4Dz2N7/w=="
    ),
    'Pb2.DEcwHisPErMsG_pb2': (
        "eNqdVWtv2kgU/e5fMUtXgqwSrx+E0EiR2mC3RbsFBCT9UKrRGI/JaO0Za2Zckf76vWMPbxSlsQTXvj7n3MfcC+/Q1V9XaClSxle3"
        "qNLZVd94nHfoM+VUEk1TlDwj/URRKYUWS5GjpMoyKoFUlCyn0kUoGqPReI7iaDj/A6ijMRp8iQf/xNHVcIQm0/F8fP/wCX2OR4Nx"
        "FANAiUou6S2KKESm356YKqn8qlZuHQMAE2MhDpo86yfB0SOVigl+i3pu6Lme02q1dvmdJpZSFxBOJkWBVkKsctooG0VWlEJqlFK1"
        "lKzUQiKiEN49vpKFSwERD6m170W+rLhmBcU/m3pq/pHvRb56LhKR45RokhBFa/6R7yzfZVxTyUm+EUoqlqe0qd3eO8eZuI8kZyBL"
        "N6cxbd7bw+g4CK4TUiQKwrg7ebj/dzi4rDG9xoReY61pt609PwVt5wIG4cOH5nQx44pKDQGgyVBMp6lDXTiOaQBOE3R30go3ohmp"
        "ct0BFFxRPBtMh5P5eGqwR8e2w7of03RGJYPif9H0E4x4J2kv+GLt9xbrbnex7l3DJzyT8qK1WJP+Yu0FAJcHZQE7+NOIeF0r4msC"
        "ToO+RvDld+ArWazDwARyD8juiCoYdB/eACfzDLzWutm9CGq6cYYVS62yv1XuWkjW8CCH8IloPIwsMjhG+iaCXhqQfi6phYVb2PVh"
        "zEKtLKRrIdoA/t6Gq/umCctVjdMnNdPzNVsbNOHCa9PZSU50JmSBhzwTtZz8TbmwaaWf7LfRxvC92tkfseV/nBT0qJe6prb2iaEl"
        "3tTODGYhg6nBJVviSubHfMjQ69XzErbN+K5ykZBcwUzaOxjXzU6698Z+pUqRFf3I05hXRbQdXNXZjfQl2ggds+ei3KOAiJU7ZJ9s"
        "IS6ToL2vyjLEhd5fHBc/zGI8wDud2S2s9O7RxbkgKU2xKM3qmhpHglPAbGS/t4Ft/hW+fRnOJvG0/cPFart8WGki9V1w83oG5eld"
        "GIQvEPAons3jyD8bqv8G5utDWhucr7LnvV3C5BD0b14vEJ7Pof/+7RKbPrzwq12ItILNUEtR0gvnfz+9334="
    ),
    'Pb2.Fo_pb2': (
        "eNqNU11v2jAUfc+vuKMP0GlY5RshIbVrYOJhUBW2l2WyEnyhlhI7sh0J9ut3HcJXW1VNpNi+Pufc63OdG2h+bcJaC6m2Iyjcpjn0"
        "keAGfqBCEzsUkOzBvSDkRju91ikkxWaDhkhZLlM0DCBcwHyxgkk4W30hqtWFWeMIpkaiEpaVTIo/+ZHY8LR3L1rBbzRWajWCLmv3"
        "WCuo1WrnrG/TCWSECDZGZ7DVepviQdkryizXxoFAuzYyd9pAbIGfl59k8VxTxmtqGfuQb/dZolMuYhcnscWS/yr2Lp9J5dCoOD0K"
        "JYVMBR5qr+Zk2/39wQsulUXjyDEqiaiNA8veBoFPx0UC4zeJWYibuEhdg1D0hJPl4/PsabV49thXhzxj2YMQSzQyTuU/FFNqcyOp"
        "RyoyVy2NavSqaHfXj3bdfrkT7VptCvlgexbSakizFvhPgz6dcn93ty4R3XmcYYXpVBgX1W7KzcFJ0x5IBKvi/b7EVPDWpXzHyyfR"
        "ruPlB+xQZ+JrK0vt1L1L21QncWrp6NWMXDkazb778SdaG2/xQYmJKrLw5I9tnJ37Bkeh1+yVzi8oJFLJXbPrlYk8T9r1SzG5uWwJ"
        "47+WE/7Iz9QljMcwJSiOAvrpTnHGde6vhT/YXCukzaPonzqfPs8m87D+l3F76ii3LjZu3Bp8Akqljnut94DLd0V7nc9gvepw+NHt"
        "zrQoUuR2rXO8Df4DAJmb0w=="
    ),
    'Pb2.GenWhisperMsg_pb2': (
        "eNqlVltv4jgYfedXeDoP0N0hCjEEWqnaaSHTot0CAjrzsKwiJ3FoNEkcOU4F++v3cxLIhVAxXaTWYM453+3E5jPq/tZFNnO8cHuL"
        "EuF2R3Kn9Rk90pByIqiDrD0SrxRFnAlmMx9ZietSDqQg8nzKFYQmczSbr5Exma4/AXU2R+MnY/ynMelOZ2ixnK/nDy/f0KMxG88n"
        "BgBilnCb3soYP169OKL8Od4qaQD4diFXCIIWe/HKQvSd8thj4S3SFawqauvq6qpI7jQrhyqAaLmcBWjL2NanmbJU9IKIcYEcGtvc"
        "iwTjiMTILD5eyDIjBhGr1HTvXT5PQuEF1HzL6kn5tb13+fE+sJhvOkQQi8Q05df2GvmKFwrKQ+IfhKzE8x2a1Z6/b9UzUb4T3wNZ"
        "epjGMvs+H0anheB1QpqwgHihsnh5+Gs6/pJi9GzBarbmS7udrw0WaLeuwQVfv2ajNb0wplyAOnQYKulkRcTXrZas3nQsdHfSB2VC"
        "XZL4ogMoeE2M1Xg5XaznS4mtzazAKveOs6Lcg8r/pc43MHfHam/Cza6HG9LcXG12o8Fmp+oACQsAwDXYtSVR7Yt9RGFnBO97SP7r"
        "wL+BxHzKAJudLv96guQw7QizNjusyehKoa7MaAy+l9tAsAepmhQaFl9oKVdu4sRzTqL3c4ib8SA4fiXCPCK1OrLXA6SwJahUDq6W"
        "U8QM4m0O6ecQUdaRhokFCaIcNDjqYAn7PRXRISvdo75zk6LESU+shp7k600eTU2VRj4JtwnZZmmH5Yy6xwakoXo4hfCTWPb5WCkH"
        "MLiXagFDHwSR2JuuVMwrpL+kWGn6mPrU4p7YZ1I9tTIbIp0nayxRwRWuK0FlV9RaMvPsnyEJ6sasjIm8wbPEm1yByzCLhHAUFzBc"
        "hx0eBE7CnzVbHJzDUwS81zX5JMgnYktP3DGo9AWmas6KEkbVEkrezkarVqZfiA1TnLv1mUV8U+YIZ0Kci1p1OFYvdIx7fr4PxEmL"
        "a5LrnzXMO4IL7qVtkOdH1murHilv8Bvxk+bDiDyViQfFY7cjuWE2nSWHPuKMnwF9+kb9E9sMThVf6a5mGzk/8kfF1Lh2onH/jG1z"
        "cwOgfEydJtBPcbbERT4RLuNB05Emzajq6VGP2/K2yUwSwxWSv4Pb5XB/Kg9yfaZxDCfNfegYYRJMjvdM3CluoC/oIFRnr1lUooBI"
        "LldlV29MM7K0dlnSc1HIRPmSU8yXlWGOzUJkdQt3b/FRMX1GHOqYLJLXrCxwxkIKmIPs320Tfrz9eJquFsay/Y9ixsdb0oSjnIs7"
        "rX8hnIbO3fBmeA5tzozV2phojUFGo1+kXRgsX3v9xqhYVz8qIOPj4aX0m+bwQ/xBvoyua6ML2Q/3k0ejMQMdq/9DI81icGkWi+X0"
        "+UwWF4+hSSN1AtYuHSRuTGGI+x8VODjxnd+1AXMSn5qxzSJ63foPo++M0w=="
    ),
    'Pb2.MajoRLoGinrEq_pb2': (
        "eNqNV/1T2zYY/j1/hQa3g/ZWH84XKTe2skI5euVjhHbrLZ1OtmRHxbZcSaZkf/1eyXISyy4HXEiwnuf90PuZXfTq5SsUC8qL9AhV"
        "Onk1M08Gu+icFUwSzSiKVkgvGSql0CIWGYqqJGESSHnJMyYDhE6v0dX1HTo7vbj7CahKVDJmR+iSfBXyg0h5ccu+BZYPpzfmHWSg"
        "m5VeigJ9YlJxURyhcTCcBOFgZ2dno7urlLIAEINEihylQqQZqyUbiTwvhdSIMhVLXmohEVEIb/59JguXAjS2qfbZk3y1yiORYUo0"
        "iYhilu896+UHvNBMFiRrBEUVzyirbXef4drevKnvAvNCManhxsAkoO7XLPViMDDqMI3QcUdxcMoSUmV6H1Dwc3o2f3t7cXN3fWuw"
        "npMbbHBC6ZxJTjL+H6PvINj70d6iWDyGo57QLnYWjwmBY/jdHAN4aF/wlD2wQmPNcwZPZovHgxGCP+H+QjtUCCidkpzhgqxBYw80"
        "MhYcRGVGdCJkjjl1wIkDwicHnVooCJqOMm50P9S55giHnuRDC0/USmmWYyUS/Z3IxozZk+AlkXQN1h50Zu/sQLOMQdFgUZrkFrI+"
        "8bBjKzYumP4u5D3Wq7IxIOpHQuwYK/B3TvXSIWOHlA45AaR0uCXj6VJboPRgNkYORkvuhDFP7WvrTAghj5lSkDOUacIz5eBJGw6X"
        "b6yc5iwXclVjwgNPsfMkLSssWQHpzqRDhv2xN8hWKMNh/5VXBf9WMTDxgcdsnSlhb97FdYrw0oH8vDuwumcZKdKKpC4q4cTzN7Go"
        "Q4hxsdE37Q+dA20FOTzsdxgyeAyviXVjC95Oyro2D+q7xuQBwkKirMG+XpcHiBsNFzI4hyKbs7iSXK/aloGu0FSNe02Uwlrcs+a2"
        "aX8trEtS0fuN86xTlsTaOWxyvKkHTAzjhSfb1fB2QdTAlx4wtlLHm2KvFAy1dp6MXnskm56gA3x8rLswVmAKxBcc1iQztF89B3Ys"
        "h/RxWnd+3HHcaWsaflfVb/2qOoSWnt/bpF3LiWwbpVzd95PedIyzmRsednlr6xaP47BN+9lyaOsqaAy9sFbWiHDk4XPJVqNHHnUM"
        "bgrSjBkc2eZy0QG5hM54JAkURUnqLvneywPb+yRLjd2a2PbzoSPL9tFG0roeLvuL2+ThkhQFy9YFe/UjFwwWWlqDu+7gXDtzOCLj"
        "Jdcs1lU9cP70LIjqGd0Ze9hsT4Yw7zc5laRc8lhhUnf/Tx6MWrkTVZVm42AQZKVjHHGtmJ0of3l93dV5HSC/2f39hJMh5MJKG0vq"
        "4WIOP6/xsRdaQcz2utkrFp4ZrjtJGL+wCuG4joqBfunLAvaoJYEtKxEG8u82BC1cHwELqRTgDSvAN5gsBdc4yUhqjnFbfzMSeILL"
        "Si0bAb77zaTkCj+UjZph55JclxOSm0tdd9zNTJiO+qNWSp7bCuihbEbdzqS+1O5oaNxor1DTHxXcklMKAX8gWeVvULDSGdcM2y6O"
        "oz2zu6aZiEimYCF1n2BXbdbf4A/zfgn7BvSDk4KeFVV+ut5a1f5mn/0FNYJ89p0otyggxIlrs/daiy0uo+HetkiebK/LAf44P8Nv"
        "8UbAHB0fo3cAZUcD+Fq0fh5A+puV3bh3JQoGh43Qf/bw5cn769sP1+cXV3tfAqzWGzd0QCL18XD8TDjsTsfheDhtw89PLs/mZ28/"
        "3l7cfe6VD5TZsym1jln41DeSXNAqY1iZBefF4H9MY/sc"
    ),
    'Pb2.MajoRLoGinrEs_pb2': (
        "eNqNU+9P2zAQ/Z6/wisfUiYatQ0UVAkJaDPWDZqqLXxZJyupr8UjsSPbQXTaH79zkv4EISIll/jee77zuxyRxtcGmUvGxbJLcrNo"
        "XNgV54jcggAVGWAkXhHzBCRT0si5TEicLxagkJRmPAHlEdIPyTCckqA/mH5B6jAkve9B72fQbwyGZDQOp+HNwzdyGwx7YT9AgJa5"
        "mkOX3Ed/pLqTSy7GoL1iA8yObMRNyGhlnqQgj6A0l6JLOp7f9JpOrVbbFve2KgYeIpyFkilZSrlMoFS2ijzNpDKEgZ4rnhmpSKQJ"
        "3X5+kkUziTvuU4u1D/kqF4anQF/Kfgr+wdqHfL1KY5lQFpkojjQU/IO1d/keFwaUiJK1UJzzhEHZe/XuHFbiPUYJR1lYuzEu85UZ"
        "dYfg9YbUl2nEhTd6uLkb9E4KTKcMfrOMVXDdKr4zAq5zjFNwdVVaS7nQoAyq4wljJ/WyCX3sOLZ7ymJy+eYcvD4sojwxdUTh1Q8m"
        "vfFgNA3HFnvg2RbrXTM2AcWx87/AvuFw12N3JmavLf+dMme1f5hTexmEti3ckprx7LXTwtu3t8STojlnmL3AXIvYRx0fpyWnCQWn"
        "o2CJrVaodoUyBUYViDMjn2ENuNgD2C0txM9VUgDEfrrVwrSxhmkTpVmp0TrblOLvqzzDqoJ0NpB5AREFoM1fqvz5br5jJTrFEfmu"
        "dWmZyDhKNB599YaurOfOu7HxHrSOlnAtWCDytL/xR9e3zp2QtdAheyqzHQqKVHL77P1Jo1ncdncl+YIIaXaHw6MPk4D26FZk0sWZ"
        "3X56NJERA0ZlZsfTNjiUAhCzlv3l0vvrH+H4LrwdDMfBxP3tUb0ZMIouKHPZ9j/PAMEuW6fnH/0eqWR5AlTPZQbHzn/9MQM6"
    ),
    'Pb2.PorTs_pb2': (
        "eNqNVNtum0AQfecrts4DThUjbFwntRQpjiGu1dRYvuSlVKsFxg4S7CJ2qZx+fYdbbJMoChIMDOecucIF6X3tkUCEEd+PSa52vZvC"
        "o12QGXDImIKQ+C9EPQNJM6FEIGLi57sdZEhK0iiGzCDEdsnC3RDHnm++IHXhkukPZ/rTsXvzBVmu3I17v30gM2cxdW0HAVLkWQBj"
        "jKEexT7iNlNsBdIoQ+D7ZWExDFm+qGfByRNkMhJ8TEaGZRqm1ul0jum9zSsEAxHaLhMJ2Quxj6FSLhSjJBWZIiHIIItSJTLCJKHH"
        "x0+yaCow4jm19H3Iz3KuogTo36qekt/yfciXL4kvYhpiu3wmoeS3fO/yjYgryDiLGyE/j+IQqtrre62difHE4ghloZnGqnpfD6Or"
        "ETzekGyRsIgby+3943x6VWJGlbHMytZG12v77hLo2iXuwd1dNVwacQmZQn3sMdbSrcqQl5pW1E9Dn9y+6YRhw47lseoiCg/bWU9X"
        "8+XGXRXY1tSOWGMShmvIIqz9H4QPuOBdX/e4d+h/ezdRr+Md2NA7mP0CZAanICQNypN7fBIEAlu1ndvouSnwpLh08TKscCaUCqMV"
        "7LHQGmXVKFVrWSXG9w7DvncYWcVZyC5YAjVj2GKMSga4PI440PmSLrFzNRbOseauxF6juhUzTptc+8PXXK1z1XYeJ/KklQcrmzho"
        "tKfV3yOkdaMwjHXdUPyiD2V7Lb2Y8T4WPoslDq6+w5k2e2vcF/YXSMn2MOGhw/PEfp2u7B7nfkUaoTZ7I9ITCorUcufs9qbS1B/o"
        "p6LRjnChTpfLoNu1Q6f0KLMe49YfHw0aCxZiG0RarHdR4kJwQEwj+1unM2fz6M7mC3uymeh/DCpf95NKxTJ1Oxh9mgA8vO1/Nz/6"
        "uBIR5jFQGYgULrX/krUYkA=="
    ),
    'Pb2.Team_msg_pb2': (
        "eNqtVmtv4jgU/c6v8Ha0gu5Os4RAgErVTguZFu0WENCZD8vKcohDo0niyHEqOr9+r2PzSMKww3SQwGCfc+4zvrxDV79doRXzgnh9"
        "jTLhX/XkTu0duqcx5URQD7mvSDxTlHAm2IqFyM18n3IgRUkQUm4gNJyg8WSBnOFo8QtQxxM0eHAGfznDq9EYTWeTxeTu6SO6d8aD"
        "ydABQMoyvqLXaEFJhKN0beTacDCVK+ij6at4ZjH6RHkasPga2YbVNJq1i4uLvV9VhzxqAKLmcxahNWPrkCplqRhECeMCeTRd8SAR"
        "jCOSIrz/+Z0snDCwWKTmeyf5PItFEFH8ouLJ+aW9k/z0NXJZiD0iiEtSmvNLe0f5RhALymMSboXcLAg9qmLX32tlT4xPJAxAlm6r"
        "MVPnuhiNGoJXhTRkEQliY/p09/do8D7H2GqxmmrVS72u12L167VLaIAPH1RVcRCnlAsQhuRCEA3lf3pZq8nAseeim0oKjCH1SRaK"
        "BqDgNXTmg9loupjMJLZUrj3WuPW8OeUBBP2Veh+hpRtufRkvN01a9HB5sdz027Bvq1PoRAn4/BykCeXLjdmC3VV+1havCYWdHnw3"
        "kfxowEdHYn5VgOXGlm9TEA1r7WDucmOBlNk1ihaMMU2h7+URkFarXFGKdfcHrZwvN60s8CoeWBriKx44YD0TgXfIVgWpxSAJGtLW"
        "EKEApgkAITshFSRKNKhT1lGwlTR2kJpuMTVLnhvriECEW0ivCPkjR9jguB3Q0OvnKFFJnf+N1Om1r51q5mq9kMTrjKyVybgYn2Xu"
        "UpVbNK0cxYsm0Wl7ps6CpeoFFLsTJeIV+1JSR0rPk2znbRCrCAp7G18WrnXYGqWAx8HqS0yicocWSkpe4Knip1pDtzon8ZdSb5Tq"
        "CeG2ZK/Lnl/TSot0Ds0OoBh4vPetV/TtoHNVOZqFou3FujnOX4fMJSGWPsJjn2pRtwj/U6bRJd6awrXjs2MF/v1/Gkqvd1JkJ5lw"
        "eUHuJCsl/k7RqZRRlTVVzt2StW2iX0iYHb92yMMhcau4y7ry9NiNsc2npfgKGNIXGlb6olNVfKYbDbMO6giBWFahca1if2Y8PLwm"
        "qibkc8RXEpaERPiMRyUzu65r2vndbdXl5FDdkMI40N9gUmzHoHEn10eapnAT3MaeE2fRcDcz0sZ+mrxHW6Eye8GSAwqIaLkiezf4"
        "cOK26odqgY9iJg5nlYGf5g4e4D1/fg3Tc//TwCEjHvUwS+S0lLGNWUwBs5X9p47hn9fCuX38/DCaT51Z/V8Dp7uBh+He5uLG7J9B"
        "obF302t2TzHw2JkvnGHrqLG++QPUM4zq1WwftW51zbeISD+s3jkS/eNu9Npv0JBedDtnKej17nZ47xz1yO60fpKe9M7uNX9AbTob"
        "PX7Du17rJ+mdnzvTOupSt2O/RWTb0Sf+9kbMy0KK0xVL6GXtP1Rfkj0="
    ),
    'Pb2.sQ_pb2': (
        "eNqVU2tvmzAU/c6v8FJppFOL8l4VqVJbYG20LYmStF/GZBm4Sa2BjYypkv36XQNpmjSKOiRz4fqc4/vyGbn8ckkiGXOxGpJCLy+v"
        "jMc6I/cgQDENMQk3RD8DyZTUMpIJCYvlEhSS0ownoBxCvAkZTxbE90aLT0gdT4j74Lvffe9yNCbT2WQxuXv8Ru79sTvxfATkslAR"
        "DImCiMMLxDR6ZtopD8DdqbF4CJlu9LMU5AlUzqUYkoHTbTktq9Fo7IJ7H1UMDiKspZIpWUm5SqBSNoo8zaTSJIY8UjzTUhGWE7r7"
        "/SCLZhJP3KeWvpN8VQjNU6AvVT4l/8B3kp9v0lAmNGaahSyHkn/gO8p3uNCgBEu2QmHBkxiq3Otv6zAS54klHGVh241ZtV83o2kR"
        "fN6RPJkyLpzp492PkXtRYgaV6bYqWxvbru2REbCtc5yCm5uqtZSLHJRGdawwZtKsksjPLctkT+OQXL+rg+PBkhWJbiIKH8+fu7PR"
        "dDGZGexBz3ZY5zaO56A4Zv4X4m843M3QDkSwbnePhBk0gvVVK1i32ghRewBkdAzLcFthxqI/oKneZIDOK3T1iKE18dU10M8l7muw"
        "HvRw9TXjSV4j+6/IMFh3jWjf2Y9FQI73ADdYCTBKg1dfp1wiEFnCNqBoweNauL0fAq5eyY00sJTmkJt+1liosTo04mXyXdvUf5XI"
        "kCU5FrX+wnpvJ8q5M/YnCrEV3IrYF0XqvVY+b+56ckG2QofshczeUFCklttn788QzcKO/VaSL4mQ+m3bHfo496lLdyLzIU7j7teh"
        "iWQxCsrMDJ5JcCwFIGYr+8umM98d+U++R92H24X928GibUeH5popfd3pfZwBIr5u9zsnCHTszxe+d/Skduv/mdsTT1y1VMZFAjSP"
        "ZAbn1j9EwR7K"
    ),
}

_FILES = {
    'emotes.json': (
        "eNp1kzESAiEMRfs9BUO9RULCAt5gGy/g2Dha2jhj5Xh3Y7nJh4riDfyfB5cl2frk8/t5e7zyKWXOa8r7/b8dNMjWJvm7Bq5EriNO"
        "Atcq4vTIKRET4mo4rzPitiMngxhyLZ4H8/XADZhvRA7OxdodA1abDASdEWmTJuyUKBPBKuycSJ/MmjWCBYLOiloZnNFp0TG72nmp"
        "Vga+Q3ZitJhBCDozIpOMhWJG2LrEv0IGLtcfZ/+8aw=="
    ),
    'emote_menu.json': (
        "eNo1kEFywyAMRfc5hcfrLiBN06SX6ahYBqaAPALX03Z69wYBy/+E4D9+T9M0q/ltmrVS81NNuib4bOFcQzbALT7XGLdLP3qp0Tim"
        "CJmSN9lRaZOXOlkYDOVMe2jwKttavTMujbxW8kGcaA3eur58ExqIloPBF9fovT1GGdOXN4V6JS3tD4SNUgTrjYfUJ3qUcJgKDgct"
        "TpbpBzoQq9Uz1iadNTWfFuS8x0iDi5jVtx5FyXybQAk7EqftrvLOK443RSlexxeLi6MjPG5nsH31LCqMEIq3j9XT3z/8yWg/"
    ),
    'singele_emote.json': (
        "eNqNljtOQ0EMRfusInp1Cv9mPMMOaNgAokFQ0iBRIfZOoPS9ll6qFEfjXB97Js+X6/3zfTx9fby+fx4P10OP2/V4fPv7umXLMFE5"
        "fm7AWeGGqDHOkVPGBXK07gBONuMmcotxiVwybiE3GbeRG4y7pwMwKKgIOgVRiVAlWp2EGO21VinayNOBIE89EaTt1gTQeJgFYZS3"
        "ZyNITzQBkI+Y6ck+mmFpmtrQDFdogSBNbdWMNwptAigcTLghGnAhyMNsBGkYFwTpUjveYnwL3RCkW+h+csL97M442Rk6PV7M/H34"
        "VZsI8vYsAJvSG0F+ewuC9DeGIkgbHnYWdASpmQgA+brGADA5iGaCNjyKGY/GTBQz7s3gRjET1rxbQ2DM+G02FEF+oiFIn8IBZtT5"
        "m17MRPdojmImZrOuY2J76JUyEkA+uGNhaZ56I0jDTIHUfAtnMePZlJ6GIF3XWcz47EpXM96B1Yw2z/AkZmjDZ8KJTZiFJ/L2bHzi"
        "6CqknPyXksVMZDNmaQjy0rgzPHVWM/u/4ZeXX7Zom4o="
    ),
}

def _dec(b): return zlib.decompress(base64.b64decode("".join(b))).decode("utf-8")

# Tulis file JSON emote di samping bot.py bila belum ada
for _n, _b in _FILES.items():
    _p = os.path.join(_HERE, _n)
    if not os.path.exists(_p):
        try:
            with open(_p, "w", encoding="utf-8") as _f: _f.write(_dec(_b))
        except Exception as _e:
            print("[!] gagal menulis", _n, _e)


class _Loader(importlib.abc.Loader):
    def create_module(self, spec): return None
    def exec_module(self, module):
        name = module.__name__
        if name == "Pb2":
            module.__path__ = []
            return
        module.__file__ = os.path.join(_HERE, name.replace(".", os.sep) + ".py")
        exec(compile(_dec(_MODULES[name]), module.__file__, "exec"), module.__dict__)


class _Finder(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path=None, target=None):
        if name == "Pb2":
            return importlib.util.spec_from_loader(name, _Loader(), is_package=True)
        if name in _MODULES:
            return importlib.util.spec_from_loader(name, _Loader())
        return None


sys.meta_path.insert(0, _Finder())

import threading, asyncio
from flask import Flask
import login_engine
import bot_core
from bot_core import TcPOnLine, TcPChaT, build_ob55_online_auth, create_auth_token_chat

PORT = int(os.environ.get("PORT", 10000))
UID = os.environ.get("GUEST_UID")
PW = os.environ.get("GUEST_PW")
REGION_PREF = os.environ.get("REGION", "IND")

if not UID or not PW:
    sys.exit("Set environment variable GUEST_UID dan GUEST_PW dulu (lihat README).")

app = Flask(__name__)


async def run_bot():
    print("[*] Starting login...")
    result = await login_engine.do_login(UID, PW, REGION_PREF)
    if not result:
        print("[-] Login gagal, coba lagi 10 detik...")
        await asyncio.sleep(10)
        return
    bot_core.bot_uid = result["bot_uid"]
    bot_core.ToKen = result["token"]
    bot_core.region = result["region"]
    key, iv, ts = result["key"], result["iv"], int(result["timestamp"])
    print(f"[+] UID: {result['bot_uid']} | Region: {result['region']} | Name: {result['account_name']}")

    chat_auth = create_auth_token_chat(int(result["bot_uid"]), result["token"], ts, key, iv)
    online_auth, _ = build_ob55_online_auth(int(result["bot_uid"]), result["token"], ts, key, iv)

    ready = asyncio.Event()
    t1 = asyncio.create_task(TcPChaT(result["chat_ip"], result["chat_port"], chat_auth, key, iv, ready, result["region"]))
    await ready.wait()
    await asyncio.sleep(1)
    t2 = asyncio.create_task(TcPOnLine(result["online_ip"], result["online_port"], key, iv, online_auth))
    print("[+] Bot online")
    await asyncio.gather(t1, t2)


async def supervisor():
    while True:  # refresh token tiap 7 jam / restart saat error
        try:
            await asyncio.wait_for(run_bot(), timeout=7 * 60 * 60)
        except asyncio.TimeoutError:
            print("[!] Token kedaluwarsa, restart...")
        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"[!] Error: {e} -> restart 5 detik")
            await asyncio.sleep(5)


@app.route("/")
def home():
    return "Bot is active"


@app.route("/healthz")
def healthz():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=PORT, use_reloader=False, threaded=True), daemon=True).start()
    try:
        asyncio.run(supervisor())
    except KeyboardInterrupt:
        print("\n[!] Dihentikan.")
PORT = int(os.environ.get("PORT", 10000))
UID = os.environ.get("GUEST_UID")
PW = os.environ.get("GUEST_PW")
REGION_PREF = os.environ.get("REGION", "IND")

if not UID or not PW:
    sys.exit("Set environment variable GUEST_UID dan GUEST_PW dulu (lihat README).")

app = Flask(__name__)


async def run_bot():
    print("[*] Starting login...")
    result = await login_engine.do_login(UID, PW, REGION_PREF)
    if not result:
        print("[-] Login gagal, coba lagi 10 detik...")
        await asyncio.sleep(10)
        return
    bot_core.bot_uid = result["bot_uid"]
    bot_core.ToKen = result["token"]
    bot_core.region = result["region"]
    key, iv, ts = result["key"], result["iv"], int(result["timestamp"])
    print(f"[+] UID: {result['bot_uid']} | Region: {result['region']} | Name: {result['account_name']}")

    chat_auth = create_auth_token_chat(int(result["bot_uid"]), result["token"], ts, key, iv)
    online_auth, _ = build_ob55_online_auth(int(result["bot_uid"]), result["token"], ts, key, iv)

    ready = asyncio.Event()
    t1 = asyncio.create_task(TcPChaT(result["chat_ip"], result["chat_port"], chat_auth, key, iv, ready, result["region"]))
    await ready.wait()
    await asyncio.sleep(1)
    t2 = asyncio.create_task(TcPOnLine(result["online_ip"], result["online_port"], key, iv, online_auth))
    print("[+] Bot online")
    await asyncio.gather(t1, t2)


async def supervisor():
    while True:  # refresh token tiap 7 jam / restart saat error
        try:
            await asyncio.wait_for(run_bot(), timeout=7 * 60 * 60)
        except asyncio.TimeoutError:
            print("[!] Token kedaluwarsa, restart...")
        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"[!] Error: {e} -> restart 5 detik")
            await asyncio.sleep(5)


@app.route("/")
def home():
    return "Bot is active"


@app.route("/healthz")
def healthz():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=PORT, use_reloader=False, threaded=True), daemon=True).start()
    try:
        asyncio.run(supervisor())
    except KeyboardInterrupt:
        print("\n[!] Dihentikan.")
