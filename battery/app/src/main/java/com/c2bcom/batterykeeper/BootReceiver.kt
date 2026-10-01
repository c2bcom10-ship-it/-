package com.c2bcom.batterykeeper

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

/** 폰을 다시 켜거나 앱을 업데이트하면, 자동 절전이 켜져 있던 경우 다시 시작해요. */
class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (Prefs(context).enabled) SaverService.start(context)
    }
}
