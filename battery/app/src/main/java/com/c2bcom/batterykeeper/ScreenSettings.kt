package com.c2bcom.batterykeeper

import android.content.Context
import android.provider.Settings

/**
 * 폰의 화면 밝기와 화면 꺼짐 시간을 바꿔요.
 * 절전을 시작할 때 원래 값을 기억해 두었다가, 평소로 돌아가면 그대로 되돌려요.
 */
class ScreenSettings(private val context: Context) {
    private val resolver = context.contentResolver
    private val backup = context.getSharedPreferences("screen_backup", Context.MODE_PRIVATE)

    fun canWrite(): Boolean = Settings.System.canWrite(context)

    fun apply(level: SaverLevel) {
        if (!canWrite()) return
        val brightness = SaverRules.brightnessFor(level)
        val timeout = SaverRules.screenTimeoutFor(level)
        if (brightness == null || timeout == null) {
            restore()
            return
        }
        backupOnce()
        Settings.System.putInt(
            resolver,
            Settings.System.SCREEN_BRIGHTNESS_MODE,
            Settings.System.SCREEN_BRIGHTNESS_MODE_MANUAL,
        )
        Settings.System.putInt(resolver, Settings.System.SCREEN_BRIGHTNESS, brightness)
        Settings.System.putInt(resolver, Settings.System.SCREEN_OFF_TIMEOUT, timeout)
    }

    private fun backupOnce() {
        if (backup.contains(KEY_TIMEOUT)) return
        backup.edit()
            .putInt(KEY_MODE, get(Settings.System.SCREEN_BRIGHTNESS_MODE, Settings.System.SCREEN_BRIGHTNESS_MODE_AUTOMATIC))
            .putInt(KEY_BRIGHTNESS, get(Settings.System.SCREEN_BRIGHTNESS, 128))
            .putInt(KEY_TIMEOUT, get(Settings.System.SCREEN_OFF_TIMEOUT, 60_000))
            .apply()
    }

    private fun restore() {
        if (!backup.contains(KEY_TIMEOUT)) return
        Settings.System.putInt(resolver, Settings.System.SCREEN_BRIGHTNESS, backup.getInt(KEY_BRIGHTNESS, 128))
        Settings.System.putInt(resolver, Settings.System.SCREEN_BRIGHTNESS_MODE, backup.getInt(KEY_MODE, 1))
        Settings.System.putInt(resolver, Settings.System.SCREEN_OFF_TIMEOUT, backup.getInt(KEY_TIMEOUT, 60_000))
        backup.edit().clear().apply()
    }

    private fun get(name: String, default: Int): Int = Settings.System.getInt(resolver, name, default)

    private companion object {
        const val KEY_MODE = "mode"
        const val KEY_BRIGHTNESS = "brightness"
        const val KEY_TIMEOUT = "timeout"
    }
}
