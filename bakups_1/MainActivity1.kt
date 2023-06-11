package com.example.app2

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.content.pm.ApplicationInfo
import android.content.pm.PackageManager
import android.content.pm.ShortcutInfo
import android.content.pm.ShortcutManager
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.drawable.AdaptiveIconDrawable
import android.graphics.drawable.BitmapDrawable
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.graphics.drawable.Drawable
import android.graphics.drawable.Icon
import android.os.Build
import android.os.Environment
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
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
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
        // AppListAdapter(this, data1, R.layout.list_item, arrayOf("name", "icon"), intArrayOf(R.id.app_name, R.id.app_icon)).createShortcuts()

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

        // Create a list of Drawables to hold the app icons
        val icons = ArrayList<Drawable>()
        val apps = packageManager.getInstalledApplications(PackageManager.GET_META_DATA)

        for (app in apps) {
            val icon = app.loadIcon(packageManager)
            icons.add(icon)
        }

        // Create a folder to save the icons
        val folder = File(Environment.getExternalStorageDirectory(), "AppIcons")
        if (!folder.exists()) {
            folder.mkdirs()
        }

        // Save the icons to the folder
        for (i in 0 until icons.size) {
            val icon = icons[i]
            val fileName = "${apps[i].packageName}.png"
            val file = File(folder, fileName)

            try {
                FileOutputStream(file).use { outputStream ->
                    val bitmap = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O && icon is AdaptiveIconDrawable) {
                        val constantState = icon.constantState
                        val drawable = constantState?.newDrawable()
                        val wrappedDrawable = DrawableCompat.wrap(drawable!!)
                        val bitmap = Bitmap.createBitmap(wrappedDrawable.intrinsicWidth, wrappedDrawable.intrinsicHeight, Bitmap.Config.ARGB_8888)
                        val canvas = Canvas(bitmap)
                        wrappedDrawable.setBounds(0, 0, canvas.width, canvas.height)
                        wrappedDrawable.draw(canvas)
                        bitmap
                    } else {
                        (icon as BitmapDrawable).bitmap
                    }

                    bitmap.compress(Bitmap.CompressFormat.PNG, 100, outputStream)
                    outputStream.flush()
                }
            } catch (e: IOException) {
                e.printStackTrace()
            }
        }

        // Create a list of maps to hold the app names and icons
        val data = ArrayList<HashMap<String, Any>>()

        for (i in 0 until icons.size) {
            val fileName = "${apps[i].packageName}.png"
            val map = HashMap<String, Any>()
            map["name"] = apps[i].loadLabel(packageManager)
            map["icon"] = fileName
            data.add(map)
        }

        // Create an adapter to display the list of apps and icons
        adapter = SimpleAdapter(
            this,
            data,
            R.layout.list_item,
            arrayOf("name", "icon"),
            intArrayOf(R.id.app_name, R.id.app_icon)
        )

        // Set the adapter on the list view
        listView.adapter = adapter
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
    private fun handleAppIconUpdate(packageName: String, newIcon: Icon) {
        val shortcutManager = context.getSystemService(ShortcutManager::class.java)
        val shortcuts = shortcutManager?.dynamicShortcuts

        if (shortcuts != null) {
            for (shortcut in shortcuts) {
                if (shortcut.intent?.component?.packageName == packageName) {
                    val updatedShortcut =
                        shortcut.shortLabel?.let {
                            shortcut.longLabel?.let { it1 ->
                                shortcut.intent?.let { it2 ->
                                    ShortcutInfo.Builder(context, shortcut.id)
                                        .setShortLabel(it)
                                        .setLongLabel(it1)
                                        .setIcon(newIcon)
                                        .setIntent(it2)
                                        .build()
                                }
                            }
                        }

                    shortcutManager.updateShortcuts(listOf(updatedShortcut))
                }
            }
        }
    }

    @RequiresApi(Build.VERSION_CODES.O)
    private fun updateAppIcon(packageName: String, newIconPath: Icon?) {
        val packageManager = context.packageManager

        try {
            val appInfo = packageManager.getApplicationInfo(packageName, PackageManager.GET_META_DATA)

            // Load the new icon
            val newIconDrawable = ContextCompat.getDrawable(context, R.drawable.icon)
            val newIconBitmap = newIconDrawable?.toBitmap()
            val newIcon = newIconBitmap?.let { Icon.createWithBitmap(it) }

            // Update the app shortcut with the new icon
            val shortcutManager = context.getSystemService(ShortcutManager::class.java)
            val appName = appInfo.loadLabel(packageManager).toString()
            val intent = packageManager.getLaunchIntentForPackage(packageName)

            val updatedShortcut = intent?.let {
                ShortcutInfo.Builder(context, "shortcut_$packageName") // Use the same ID to identify the shortcut
                    .setShortLabel(appName)
                    .setIcon(newIcon)
                    .setIntent(it)
                    .build()
            }

            if (updatedShortcut != null) {
                shortcutManager?.updateShortcuts(listOf(updatedShortcut)) // Update only the specific shortcut
            }

            Toast.makeText(context, "App icon updated", Toast.LENGTH_SHORT).show()
        } catch (e: PackageManager.NameNotFoundException) {
            e.printStackTrace()
            Toast.makeText(context, "Failed to update app icon", Toast.LENGTH_SHORT).show()
        }
    }

    @RequiresApi(Build.VERSION_CODES.N_MR1)
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


