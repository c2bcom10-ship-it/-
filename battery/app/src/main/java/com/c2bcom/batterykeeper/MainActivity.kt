package com.c2bcom.batterykeeper

import android.Manifest
import android.app.Activity
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.PowerManager
import android.provider.Settings
import android.widget.Button
import android.widget.SeekBar
import android.widget.Switch
import android.widget.TextView

class MainActivity : Activity() {
    private lateinit var prefs: Prefs
    private lateinit var screen: ScreenSettings

    private lateinit var percentText: TextView
    private lateinit var statusText: TextView
    private lateinit var permissionText: TextView
    private lateinit var permissionButton: Button
    private lateinit var powerSaveText: TextView
    private lateinit var saveAtText: TextView
    private lateinit var saveAtBar: SeekBar
    private lateinit var autoSwitch: Switch

    private val batteryReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) = refresh(BatteryInfo.from(intent))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        prefs = Prefs(this)
        screen = ScreenSettings(this)

        percentText = findViewById(R.id.percentText)
        statusText = findViewById(R.id.statusText)
        permissionText = findViewById(R.id.permissionText)
        permissionButton = findViewById(R.id.permissionButton)
        powerSaveText = findViewById(R.id.powerSaveText)
        saveAtText = findViewById(R.id.saveAtText)
        saveAtBar = findViewById(R.id.saveAtBar)
        autoSwitch = findViewById(R.id.autoSwitch)

        // 막대 0~6 → 20%, 25%, ... 50%
        saveAtBar.max = 6
        saveAtBar.progress = (prefs.saveAt - 20) / 5
        showSaveAt()
        saveAtBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(bar: SeekBar, progress: Int, fromUser: Boolean) {
                prefs.saveAt = 20 + progress * 5
                showSaveAt()
            }
            override fun onStartTrackingTouch(bar: SeekBar) {}
            override fun onStopTrackingTouch(bar: SeekBar) {
                // 새 기준을 바로 적용하려고 서비스를 다시 시작해요.
                if (prefs.enabled) {
                    SaverService.stop(this@MainActivity)
                    SaverService.start(this@MainActivity)
                }
            }
        })

        autoSwitch.isChecked = prefs.enabled
        autoSwitch.setOnCheckedChangeListener { _, checked ->
            prefs.enabled = checked
            if (checked) SaverService.start(this) else SaverService.stop(this)
        }

        permissionButton.setOnClickListener {
            startActivity(Intent(Settings.ACTION_MANAGE_WRITE_SETTINGS, Uri.parse("package:$packageName")))
        }
        findViewById<Button>(R.id.batterySaverButton).setOnClickListener {
            startActivity(Intent(Settings.ACTION_BATTERY_SAVER_SETTINGS))
        }

        if (Build.VERSION.SDK_INT >= 33) {
            requestPermissions(arrayOf(Manifest.permission.POST_NOTIFICATIONS), 0)
        }
    }

    override fun onResume() {
        super.onResume()
        // 처음 등록하면 지금 배터리 상태가 바로 한 번 들어와요.
        refresh(BatteryInfo.from(registerReceiver(batteryReceiver, IntentFilter(Intent.ACTION_BATTERY_CHANGED))))
    }

    override fun onPause() {
        unregisterReceiver(batteryReceiver)
        super.onPause()
    }

    private fun showSaveAt() {
        saveAtText.text = "배터리가 ${prefs.saveAt}% 이하면 절전, ${SaverRules.STRONG_AT}% 이하면 강력 절전"
    }

    private fun refresh(info: BatteryInfo?) {
        if (info != null) {
            percentText.text = "${info.percent}%"
            val charging = if (info.charging) "충전 중이에요 ⚡" else "충전하고 있지 않아요"
            val mode = if (prefs.enabled) "지금 단계: ${prefs.currentLevel.label}" else "자동 절전이 꺼져 있어요"
            statusText.text = "$charging\n$mode"
        }

        val canWrite = screen.canWrite()
        permissionText.text = if (canWrite) {
            "✅ 화면 설정 권한이 있어요"
        } else {
            "⚠️ 화면 밝기를 바꾸려면 권한이 필요해요"
        }
        permissionButton.isEnabled = !canWrite

        val powerSave = getSystemService(PowerManager::class.java).isPowerSaveMode
        powerSaveText.text = if (powerSave) "폰의 절전 모드: 켜짐" else "폰의 절전 모드: 꺼짐"
    }
}
