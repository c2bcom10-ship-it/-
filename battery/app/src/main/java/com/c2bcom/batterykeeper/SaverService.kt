package com.c2bcom.batterykeeper

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.IBinder

/**
 * 뒤에서 계속 돌면서 배터리가 바뀔 때마다 절전 단계를 정해요.
 * 배터리 % 가 바뀔 때만 깨어나서 일하기 때문에, 이 서비스 자체는 배터리를 거의 안 써요.
 */
class SaverService : Service() {
    private lateinit var prefs: Prefs
    private lateinit var screen: ScreenSettings

    private val batteryReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
            BatteryInfo.from(intent)?.let(::onBatteryChanged)
        }
    }

    override fun onCreate() {
        super.onCreate()
        prefs = Prefs(this)
        screen = ScreenSettings(this)
        createChannel()
        startForeground(NOTIFICATION_ID, buildNotification("배터리를 확인하고 있어요…"))
        registerReceiver(batteryReceiver, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int = START_STICKY

    override fun onDestroy() {
        unregisterReceiver(batteryReceiver)
        screen.apply(SaverLevel.NORMAL)
        prefs.currentLevel = SaverLevel.NORMAL
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun onBatteryChanged(info: BatteryInfo) {
        val level = SaverRules.decide(info.percent, info.charging, prefs.saveAt)
        if (level != prefs.currentLevel) {
            screen.apply(level)
            prefs.currentLevel = level
        }
        val charging = if (info.charging) " · 충전 중" else ""
        val text = "🔋 ${info.percent}%$charging · ${level.label} 모드"
        getSystemService(NotificationManager::class.java).notify(NOTIFICATION_ID, buildNotification(text))
    }

    private fun createChannel() {
        val channel = NotificationChannel(CHANNEL_ID, "자동 절전", NotificationManager.IMPORTANCE_LOW)
        getSystemService(NotificationManager::class.java).createNotificationChannel(channel)
    }

    private fun buildNotification(text: String): Notification {
        val openApp = PendingIntent.getActivity(
            this, 0, Intent(this, MainActivity::class.java), PendingIntent.FLAG_IMMUTABLE,
        )
        return Notification.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_battery)
            .setContentTitle(getString(R.string.app_name))
            .setContentText(text)
            .setContentIntent(openApp)
            .setOngoing(true)
            .build()
    }

    companion object {
        private const val CHANNEL_ID = "auto_saver"
        private const val NOTIFICATION_ID = 1

        fun start(context: Context) {
            context.startForegroundService(Intent(context, SaverService::class.java))
        }

        fun stop(context: Context) {
            context.stopService(Intent(context, SaverService::class.java))
        }
    }
}
