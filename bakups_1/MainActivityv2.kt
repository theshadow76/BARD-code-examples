package com.example.app2

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.content.pm.ApplicationInfo
import android.content.pm.PackageManager
import android.content.pm.ShortcutInfo
import android.content.pm.ShortcutManager
import android.graphics.Bitmap
import android.graphics.drawable.AdaptiveIconDrawable
import android.graphics.drawable.BitmapDrawable
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.graphics.drawable.Drawable
import android.graphics.drawable.Icon
import android.os.Build
import android.util.Log
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.ListView
import android.widget.SimpleAdapter
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AlertDialog
import androidx.core.content.ContextCompat
import androidx.core.graphics.drawable.DrawableCompat
import androidx.core.graphics.drawable.toBitmap
import java.util.ArrayList
import java.util.HashMap

class MainActivity : AppCompatActivity() {

    private lateinit var listView: ListView
    private lateinit var adapter: SimpleAdapter
    private lateinit var apps: List<ApplicationInfo>

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Create the shortcuts
        val data1 = getInstalledApps()
        val packageNames = data1.map { it["packageName"] as String } // Extract package names from data
        adapter = AppListAdapter(this, data1, R.layout.list_item, arrayOf("name", "icon"), intArrayOf(R.id.app_name, R.id.app_icon), packageNames, this)
        (adapter as AppListAdapter).createShortcuts()

        listView = findViewById(R.id.list_view)
        listView.adapter = adapter

        apps = packageManager.getInstalledApplications(PackageManager.GET_META_DATA) // Initialize apps here

        listView.setOnItemClickListener { _, _, position, _ ->
            AlertDialog.Builder(this)
                .setTitle("Are you sure?")
                .setMessage("Are you sure you want to create a shortcut with a custom icon for this app?")
                .setPositiveButton("YES") { _, _ ->
                    val shortcutIntent = packageManager.getLaunchIntentForPackage(apps[position].packageName)
                    val addIntent = Intent()
                    addIntent.putExtra(Intent.EXTRA_SHORTCUT_INTENT, shortcutIntent)
                    addIntent.putExtra(Intent.EXTRA_SHORTCUT_NAME, apps[position].name)
                    addIntent.putExtra(Intent.EXTRA_SHORTCUT_ICON_RESOURCE, Intent.ShortcutIconResource.fromContext(this, R.drawable.icon))
                    addIntent.action = "com.android.launcher.action.INSTALL_SHORTCUT"
                    sendBroadcast(addIntent)
                }
                .setNegativeButton("NO", null)
                .show()
        }
    }

    fun getInstalledApps(): List<Map<String, Any>> {
        val packageManager = this.packageManager
        val apps = packageManager.getInstalledApplications(PackageManager.GET_META_DATA)

        val data = mutableListOf<Map<String, Any>>()
        for (app in apps) {
            val map = mutableMapOf<String, Any>()
            map["name"] = app.loadLabel(packageManager)
            map["packageName"] = app.packageName
            map["icon"] = app.loadIcon(packageManager)
            Log.d("AppListAdapter", "Icon for ${app.packageName}: ${map["icon"]}")
            data.add(map)
        }

        return data
    }
}

class AppListAdapter(
    private val context: Context,
    private val data: List<Map<String, Any>>,
    private val resource: Int,
    private val from: Array<String>,
    private val to: IntArray,
    private val packageNames: List<String>,
    private val activity: Activity // Add activity as a parameter
) : SimpleAdapter(context, data, resource, from, to) {

    @RequiresApi(Build.VERSION_CODES.O)
    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        val view = super.getView(position, convertView, parent)

        val iconView = view.findViewById<ImageView>(R.id.app_icon)
        val iconDrawable = data[position]["icon"] as? Drawable // Get the icon Drawable

        if (iconDrawable != null) {
            iconView.setImageDrawable(iconDrawable)
            Log.d("AppListAdapter", "Setting icon for position $position: $iconDrawable")
        } else {
            Log.d("AppListAdapter", "No icon for position $position")
        }

        val packageName = packageNames[position] // Get the packageName from the list

        view.setOnClickListener {
            AlertDialog.Builder(activity) // Use activity here
                .setTitle("Change Icon")
                .setMessage("Do you want to change the icon of this app?")
                .setPositiveButton("Yes") { _, _ ->
                    // ...
                }
                .setNegativeButton("No", null)
                .show()
        }

        return view
    }

    @RequiresApi(Build.VERSION_CODES.O)
    fun createShortcuts() {
        val shortcutManager = context.getSystemService(ShortcutManager::class.java)

        // Create a list to hold the shortcuts
        val shortcutList = mutableListOf<ShortcutInfo>()

        // Load the custom icon
        val newIconDrawable = ContextCompat.getDrawable(context, R.drawable.icon)
        val newIconBitmap = newIconDrawable?.toBitmap()
        val newIcon = newIconBitmap?.let { Icon.createWithBitmap(it) }

        // Loop through each app and create a shortcut
        for (i in 0 until minOf(data.size, 5)) {  // Limit to 5 apps
            val app = data[i]
            val packageName = app["packageName"] as String
            val appName = app["name"] as String
            val intent = context.packageManager.getLaunchIntentForPackage(packageName)

            val shortcut = intent?.let {
                ShortcutInfo.Builder(context, "shortcut_$packageName") // Set a unique ID for the shortcut
                    .setShortLabel(appName)
                    .setIcon(newIcon)
                    .setIntent(it)
                    .build()
            }

            if (shortcut != null) {
                shortcutList.add(shortcut)
            }
        }

        // Add the shortcuts to the shortcut manager
        shortcutManager?.dynamicShortcuts = shortcutList
    }
}
