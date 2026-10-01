package com.c2bcom.batterykeeper

/** 절전 단계. 숫자가 클수록 더 많이 아껴요. */
enum class SaverLevel(val label: String) {
    NORMAL("평소"),
    SAVE("절전"),
    STRONG("강력 절전"),
}

/**
 * "배터리가 몇 %일 때 어떤 단계로 갈지"를 정하는 규칙이에요.
 * 안드로이드 기능을 쓰지 않아서 테스트하기 쉬워요.
 */
object SaverRules {
    /** 이 % 이하가 되면 무조건 강력 절전이에요. */
    const val STRONG_AT = 15

    fun decide(percent: Int, charging: Boolean, saveAt: Int): SaverLevel = when {
        charging -> SaverLevel.NORMAL
        percent <= STRONG_AT -> SaverLevel.STRONG
        percent <= saveAt -> SaverLevel.SAVE
        else -> SaverLevel.NORMAL
    }

    /** 화면 밝기 (0~255). null이면 원래 값으로 돌려놔요. */
    fun brightnessFor(level: SaverLevel): Int? = when (level) {
        SaverLevel.NORMAL -> null
        SaverLevel.SAVE -> 80
        SaverLevel.STRONG -> 25
    }

    /** 화면이 꺼지기까지 시간 (밀리초). null이면 원래 값으로 돌려놔요. */
    fun screenTimeoutFor(level: SaverLevel): Int? = when (level) {
        SaverLevel.NORMAL -> null
        SaverLevel.SAVE -> 30_000
        SaverLevel.STRONG -> 15_000
    }
}
