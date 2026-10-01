package com.c2bcom.batterykeeper

import android.content.Intent
import android.os.BatteryManager

/** 배터리 방송(Intent)에서 % 와 충전 중인지를 꺼내요. */
data class BatteryInfo(val percent: Int, val charging: Boolean) {
    companion object {
        fun from(intent: Intent?): BatteryInfo? {
            if (intent == null) return null
            val level = intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
            val scale = intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
            if (level < 0 || scale <= 0) return null
            val plugged = intent.getIntExtra(BatteryManager.EXTRA_PLUGGED, 0)
            return BatteryInfo(level * 100 / scale, plugged != 0)
        }
    }
}
