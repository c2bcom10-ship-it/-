package com.c2bcom.batterykeeper

import org.junit.Assert.assertEquals
import org.junit.Test

class SaverRulesTest {
    @Test
    fun chargingIsAlwaysNormal() {
        assertEquals(SaverLevel.NORMAL, SaverRules.decide(5, charging = true, saveAt = 30))
    }

    @Test
    fun aboveSaveAtIsNormal() {
        assertEquals(SaverLevel.NORMAL, SaverRules.decide(31, charging = false, saveAt = 30))
    }

    @Test
    fun atOrBelowSaveAtIsSave() {
        assertEquals(SaverLevel.SAVE, SaverRules.decide(30, charging = false, saveAt = 30))
        assertEquals(SaverLevel.SAVE, SaverRules.decide(16, charging = false, saveAt = 30))
    }

    @Test
    fun atOrBelowStrongAtIsStrong() {
        assertEquals(SaverLevel.STRONG, SaverRules.decide(15, charging = false, saveAt = 30))
        assertEquals(SaverLevel.STRONG, SaverRules.decide(1, charging = false, saveAt = 50))
    }

    @Test
    fun normalRestoresOriginalSettings() {
        assertEquals(null, SaverRules.brightnessFor(SaverLevel.NORMAL))
        assertEquals(null, SaverRules.screenTimeoutFor(SaverLevel.NORMAL))
    }
}
