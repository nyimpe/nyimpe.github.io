// Numbers follow the roguelike plan posts 4, 6, 7, 8, 9 and 10 (village only).

export const NABI = { name: "나비", hp: 30, speed: 10, face: "nabi-face" };

export const SKILLS = {
  scratch: { name: "할퀴기", kind: "공격", text: "피해 6", damage: 6 },
  crouch: { name: "웅크리기", kind: "막기", text: "막기 6", block: 6 },
};

// action: [label, kind, value]
// kinds: atk, confuse, block, shield, guard (block to partner), charge (next atk is value),
// summon, heal, steal (Nabi slow -2 for two turns), flee_prep, flee
export const YOKAI = {
  dokkaebi: {
    name: "도깨비", hp: 10, speed: 12, sheet: "dokkaebi", face: "dokkaebi-face", body: "character",
    weights: [[50, "방망이", "atk", 4], [30, "장난", "confuse", 0], [20, "숨기", "block", 4]],
  },
  dog: {
    name: "귀구", hp: 8, speed: 10, sheet: "dog", face: "dog-face", body: "animal",
    weights: [[60, "물기", "atk", 3], [40, "지키기", "guard", 4]],
  },
  toad: {
    name: "금두꺼비", hp: 14, speed: 8, sheet: "toad", face: "toad-face", body: "animal", bonusCoins: 3,
    weights: [[50, "혀 치기", "atk", 4], [30, "금빛 울음", "shield", 4], [20, "행운 모으기", "charge", 8]],
  },
  bjm: {
    name: "백죽모", hp: 22, speed: 10, sheet: "oldman", face: "oldman-face", body: "character", elite: true, leader: true,
    loop: [["밥 내놔!", "summon", "mob"], ["대나무 지팡이", "atk", 5], ["대나무 지팡이", "atk", 5]],
    blurb: "무리는 하나까지 부른다. 대장이 항복하면 무리도 물러난다",
  },
  mob: {
    name: "따라온 무리", hp: 5, speed: 10, sheet: "mob", face: "mob-face", body: "character", summon: true,
    loop: [["보채기", "atk", 2]],
  },
  guup: {
    name: "구업", hp: 26, speed: 10, sheet: "donkey", face: "donkey-face", body: "animal", elite: true,
    loop: [["들이받기", "atk", 9], ["흰죽 먹기", "heal", 5], ["창고 지키기", "block", 8]],
    blurb: "부잣집 창고를 지키는 망아지. 오래 버틴다",
  },
  yagwang: {
    name: "야광", hp: 20, speed: 12, sheet: "spirit", face: "spirit-face", body: "character", elite: true,
    loop: [["신발 훔치기", "steal", 2], ["할퀴기", "atk", 4], ["할퀴기", "atk", 4], ["할퀴기", "atk", 4],
      ["도망 준비", "flee_prep", 0], ["도망", "flee", 0]],
    blurb: "신발 도둑. 도망치면 보상이 없다. 막지 말고 쉬지 않고 쳐라",
  },
  kim: {
    name: "도깨비 김서방", hp: 40, speed: 10, sheet: "boss-idle", face: "boss-face", body: "boss", boss: true,
    loop: [["방망이", "atk", 8], ["장난", "confuse", 0], ["숨기", "block", 10]],
  },
};

export const GROUPS = [
  { ids: ["dokkaebi"], coins: 4 },
  { ids: ["dog", "dog"], coins: 6 },
  { ids: ["toad"], coins: 4 },
  { ids: ["toad", "dog"], coins: 6 },
];

export const ELITES = ["bjm", "guup", "yagwang"];

export const RELICS = {
  branch: { name: "붉나무 가지", icon: "branch", text: "전투를 시작할 때 막기 4" },
  feather: { name: "베개 속 닭", icon: "feather", text: "전투를 시작할 때 첫 차례를 5 당긴다" },
  iron: { name: "철마", icon: "iron", text: "레벨업 회복이 3에서 8로" },
  porridge: { name: "흰죽 한 그릇", icon: "onigiri", text: "전투에서 이기면 체력 2 회복" },
  scale: { name: "용손의 비늘", icon: "gem", text: "이름난 요괴를 이길 때마다 최대 체력 +4" },
  bamboo: { name: "대나무 잎", icon: "grass", text: "체력이 처음 절반 아래가 되면 막기 10 (전투마다 한 번)" },
};

export const TALENTS = [
  { id: "dokkaebi", name: "도깨비 재주", from: "도깨비", face: "dokkaebi-face", does: "적을 헷갈리게 해 행동을 바꾼다", first: "장난 · 피해 3, 헷갈림", road: "상점 값 20% 할인" },
  { id: "dog", name: "개 재주", from: "귀구", face: "dog-face", does: "막고, 막은 만큼 되갚는다", first: "되갚기 · 막기 8", road: "이름난 요괴를 미리 안다" },
  { id: "horse", name: "말 재주", from: "용마", face: "horse-face", does: "먼저 움직이고 여러 번 친다", first: "돌진 · 피해 14", road: "칸 하나를 건너뛴다" },
  { id: "turtle", name: "거북 재주", from: "현구", face: null, does: "흰 기운으로 지키고 낫게 한다", first: "등껍질 · 보호막 6", road: "쉬는 칸에서 더 회복한다" },
];

export const REWARD = {
  fight: { xp: 3 },
  elite: { xp: 6, coins: 10 },
  boss: { xp: 10, coins: 15 },
};
