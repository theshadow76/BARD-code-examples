package com.example.app2

import android.content.Context
import android.content.pm.ApplicationInfo
import android.content.pm.PackageManager
import android.content.pm.ShortcutInfo
import android.content.pm.ShortcutManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.drawable.BitmapDrawable
import android.graphics.drawable.Drawable
import android.graphics.drawable.Icon
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.ImageView
import android.widget.ListView
import android.widget.TextView
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.core.graphics.drawable.toBitmap
import androidx.fragment.app.Fragment
import com.example.app2.R
import java.io.File
import java.io.FileOutputStream

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Add the AppListFragment to the activity
        val appListFragment = AppListFragment()
        supportFragmentManager.beginTransaction()
            .add(R.id.fragment_container, appListFragment)
            .commit()
    }
}


class AppListFragment : Fragment() {

    private lateinit var listView: ListView
    private lateinit var data: List<Map<String, Any>>

    // Add the function here
    private fun drawableToBitmap(drawable: Drawable): Bitmap {
        if (drawable is BitmapDrawable) {
            return drawable.bitmap
        }
        val bitmap = Bitmap.createBitmap(drawable.intrinsicWidth, drawable.intrinsicHeight, Bitmap.Config.ARGB_8888)
        val canvas = Canvas(bitmap)
        drawable.setBounds(0, 0, canvas.width, canvas.height)
        drawable.draw(canvas)
        return bitmap
    }

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_app_list, container, false)

        // Get the list view
        listView = view.findViewById(R.id.list_view)

        // Populate the data
        data = getInstalledApps(requireContext())

        // Set the adapter
        listView.adapter = AppListAdapter(requireContext(), data)

        // Set the click listener
        listView.setOnItemClickListener { _, _, position, _ ->
            Log.d("AppListFragment", "Item clicked: $position")
            val app = data[position]
            val packageName = app["packageName"] as String
            val intent = requireContext().packageManager.getLaunchIntentForPackage(packageName)
            if (intent == null) {
                Log.d("AppListFragment", "No launch intent for package: $packageName")
                return@setOnItemClickListener
            }

            try {
                // Create an AlertDialog.Builder to build the dialog
                val builder = AlertDialog.Builder(requireContext())
                builder.setTitle("Change Shortcut Icon?")
                builder.setMessage("Would you like to change the shortcut icon for this app?")

                // Set the positive (yes) button
                builder.setPositiveButton("Yes") { _, _ ->
                    // Change the shortcut icon
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                        changeShortcutIcon(requireContext(), packageName)
                    }
                    // Launch the app
                    startActivity(intent)
                }

                // Set the negative (no) button
                builder.setNegativeButton("No") { _, _ ->
                    // Launch the app
                    startActivity(intent)
                }

                // Show the dialog
                builder.show()
            } catch (e: Exception) {
                Log.e("AppListFragment", "Error showing AlertDialog", e)
            }

        }


        // Create the shortcuts
        createShortcuts()

        return view
    }

    @RequiresApi(Build.VERSION_CODES.O)
    fun changeShortcutIcon(context: Context, packageName: String) {
        val shortcutManager = context.getSystemService(ShortcutManager::class.java)

        // Load the custom icon
        val newIconDrawable = ContextCompat.getDrawable(context, R.drawable.icon) // Use your custom icon here
        val newIconBitmap = newIconDrawable?.toBitmap()
        val newIcon = newIconBitmap?.let { Icon.createWithBitmap(it) }

        // Get the list of existing shortcuts for the app
        val shortcuts = shortcutManager?.getDynamicShortcuts()

        // Change the icon for each shortcut
        for (shortcut in shortcuts ?: emptyList()) {
            if (shortcut.intent?.`package` == packageName) {
                val updatedShortcut = shortcut.intent?.let {
                    ShortcutInfo.Builder(context, shortcut.id)
                        .setShortLabel(shortcut.shortLabel.toString())
                        .setIcon(newIcon)
                        .setIntent(it)
                        .build()
                }

                shortcutManager?.updateShortcuts(listOf(updatedShortcut))
            }
        }
    }


    private fun getInstalledApps(context: Context): List<Map<String, Any>> {
        val pm = context.packageManager
        val packages = pm.getInstalledPackages(PackageManager.GET_META_DATA)
        val appList = mutableListOf<Map<String, Any>>()

        for (packageInfo in packages) {
            // Do not filter any apps, include all
            val appName = packageInfo.applicationInfo.loadLabel(pm).toString()
            val packageName = packageInfo.packageName
            val appIcon = packageInfo.applicationInfo.loadIcon(pm)

            val app = mapOf(
                "name" to appName,
                "packageName" to packageName,
                "icon" to appIcon
            )

            appList.add(app)
        }

        return appList
    }


    @RequiresApi(Build.VERSION_CODES.O)
    private fun createShortcuts() {
        val shortcutManager = requireContext().getSystemService(ShortcutManager::class.java)

        // Create a list to hold the shortcuts
        val shortcutList = mutableListOf<ShortcutInfo>()

        // Load the custom icon
        val newIconDrawable = ContextCompat.getDrawable(requireContext(), R.drawable.icon)
        val newIconBitmap = newIconDrawable?.toBitmap()
        val newIcon = newIconBitmap?.let { Icon.createWithBitmap(it) }

        // Download the icons and create the shortcuts
        for (i in 0 until minOf(data.size, 5)) {  // Limit to 5 apps
            val app = data[i]
            val packageName = app["packageName"] as String
            val appName = app["name"] as String

            // Download the icon
            val iconDir = File(requireContext().filesDir, "icons")
            if (!iconDir.exists()) {
                iconDir.mkdir()
            }

            val iconFile = File(iconDir, "$packageName.png")
            val iconStream = FileOutputStream(iconFile)

            val iconBitmap = drawableToBitmap(app["icon"] as Drawable)

            iconBitmap.compress(Bitmap.CompressFormat.PNG, 100, iconStream)

            iconStream.flush()
            iconStream.close()

            // Create the shortcut
            val intent = requireContext().packageManager.getLaunchIntentForPackage(packageName)

            val shortcut = intent?.let {
                ShortcutInfo.Builder(requireContext(), "shortcut_$packageName") // Set a unique ID for the shortcut
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

    private class AppListAdapter(
        private val context: Context,
        private val data: List<Map<String, Any>>
    ) : BaseAdapter() {

        private val inflater = LayoutInflater.from(context)

        override fun getCount(): Int {
            return data.size
        }

        override fun getItem(position: Int): Any {
            return data[position]
        }

        override fun getItemId(position: Int): Long {
            return position.toLong()
        }

        override fun getView(position: Int, convertView: View?, parent: ViewGroup?): View {
            val view = convertView ?: inflater.inflate(R.layout.list_item, parent, false)

            // Get the app data
            val app = data[position]
            val appName = app["name"] as String
            val packageName = app["packageName"] as String

            // Set the app name
            val appNameView = view.findViewById<TextView>(R.id.app_name)
            appNameView.text = appName

            // Set the app icon
            val appIconView = view.findViewById<ImageView>(R.id.app_icon)

            val iconDir = File(context.filesDir, "icons")
            val iconFile = File(iconDir, "$packageName.png")
            if (iconFile.exists()) {
                val iconBitmap = BitmapFactory.decodeFile(iconFile.absolutePath)
                appIconView.setImageBitmap(iconBitmap)
            } else {
                appIconView.setImageDrawable(app["icon"] as Drawable)
            }

            return view
        }
    }
}
