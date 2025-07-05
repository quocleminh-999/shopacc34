# Tiếng Việt
VIETNAMESE_SURNAMES = [
    "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan",
    "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương",
    "Lý", "Tạ", "Cao", "Mai", "Hà", "Đoàn", "Lâm", "Trương",
    "Văn", "Đinh", "Đinh", "Kiều"
]

VIETNAMESE_MIDDLE_NAMES = [
    "Thị", "Văn", "Hữu", "Đức", "Ngọc", "Thanh", "Trọng", 
    "Phúc", "Anh", "Quang", "Minh", "Hoàng", "Duy", "Xuân"
]

VIETNAMESE_FIRST_NAMES = [
    "An", "Bình", "Châu", "Dương", "Giang", "Hà", "Hải",
    "Hùng", "Hương", "Hồng", "Khanh", "Khánh", "Lan", "Linh",
    "Long", "Minh", "My", "Nam", "Ngọc", "Nhung", "Phong",
    "Quân", "Quỳnh", "Sơn", "Tâm", "Tân", "Thảo", "Thành",
    "Thắng", "Thu", "Thúy", "Trang", "Trinh", "Trung", "Tuấn", 
    "Vân", "Vi", "Vy", "Yến"
]

# Tiếng Anh
ENGLISH_SURNAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
]

ENGLISH_FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard",
    "Joseph", "Thomas", "Charles", "Mary", "Patricia", "Jennifer", "Linda",
    "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"
]

# Tiếng Nhật
JAPANESE_SURNAMES = [
    "Sato", "Suzuki", "Takahashi", "Tanaka", "Watanabe", "Ito", "Yamamoto",
    "Nakamura", "Kobayashi", "Kato", "Yoshida", "Yamada", "Sasaki", "Yamaguchi",
    "Saito", "Matsumoto", "Inoue", "Kimura", "Hayashi", "Shimizu"
]

JAPANESE_FIRST_NAMES = [
    "Hiroto", "Yuto", "Haruto", "Sota", "Yuki", "Kento", "Riku",
    "Yamato", "Tsubasa", "Kenji", "Akira", "Daiki", "Kazuki", "Takumi",
    "Yui", "Hana", "Aoi", "Sakura", "Ichika", "Akari"
]

# Tiếng Hàn
KOREAN_SURNAMES = [
    "Kim", "Lee", "Park", "Choi", "Jung", "Kang", "Cho",
    "Yoon", "Jang", "Lim", "Han", "Shin", "Seo", "Oh",
    "Song", "Baek", "Kwon", "Jeong", "Hwang", "Ko"
]

KOREAN_FIRST_NAMES = [
    "Min-jun", "Seo-jun", "Ji-hoon", "Min-ho", "Ji-min", "Seo-yeon",
    "Ji-yeon", "Min-seo", "Ji-woo", "Seo-jin", "Min-ji", "Ji-hye",
    "Seo-hyeon", "Min-hyeon", "Ji-seo", "Seo-min", "Min-woo", "Ji-ho",
    "Seo-ho", "Min-hye"
]

# Tiếng Lào
LAO_SURNAMES = [
    "Phommasak", "Sisoulith", "Thammavong", "Souvanthong", "Phanthavong",
    "Sisavath", "Phommachanh", "Souliya", "Phanthavong", "Sisoulith",
    "Thammavong", "Souvanthong", "Phommasak", "Sisavath", "Phommachanh"
]

LAO_FIRST_NAMES = [
    "Somsak", "Bounthong", "Khamphou", "Souvanthong", "Phanthavong",
    "Sisavath", "Phommachanh", "Souliya", "Phanthavong", "Sisoulith",
    "Thammavong", "Souvanthong", "Phommasak", "Sisavath", "Phommachanh"
]

# Danh sách các loại tên
NAME_TYPES = {
    "vietnamese": {
        "surnames": VIETNAMESE_SURNAMES,
        "middle_names": VIETNAMESE_MIDDLE_NAMES,
        "first_names": VIETNAMESE_FIRST_NAMES
    },
    "english": {
        "surnames": ENGLISH_SURNAMES,
        "middle_names": [],
        "first_names": ENGLISH_FIRST_NAMES
    },
    "japanese": {
        "surnames": JAPANESE_SURNAMES,
        "middle_names": [],
        "first_names": JAPANESE_FIRST_NAMES
    },
    "korean": {
        "surnames": KOREAN_SURNAMES,
        "middle_names": [],
        "first_names": KOREAN_FIRST_NAMES
    },
    "lao": {
        "surnames": LAO_SURNAMES,
        "middle_names": [],
        "first_names": LAO_FIRST_NAMES
    }
} 