package com.c2bcom.batterykeeper

import android.content.Context

/** 앱 설정을 폰에 저장해요. */
class Prefs(context: Context) {
    private val sp = context.getSharedPreferences("battery_keeper", Context.MODE_PRIVATE)

    var enabled: Boolean
        get() = sp.getBoolean("enabled", false)
        set(value) = sp.edit().putBoolean("enabled", value).apply()

    /** 이 % 이하가 되면 절전을 시작해요. */
    var saveAt: Int
        get() = sp.getInt("save_at", 30)
        set(value) = sp.edit().putInt("save_at", value).apply()

    var currentLevel: SaverLevel
        get() = SaverLevel.valueOf(sp.getString("current_level", SaverLevel.NORMAL.name)!!)
        set(value) = sp.edit().putString("current_level", value.name).apply()
}
