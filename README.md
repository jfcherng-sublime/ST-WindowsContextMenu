# ST-WindowsContextMenu

[![Required ST Build](https://img.shields.io/badge/ST-4105+-orange.svg?style=flat-square&logo=sublime-text)](https://www.sublimetext.com)
[![GitHub Actions](https://img.shields.io/github/workflow/status/jfcherng-sublime/ST-WindowsContextMenu/Python?style=flat-square)](https://github.com/jfcherng-sublime/ST-WindowsContextMenu/actions)
[![Package Control](https://img.shields.io/packagecontrol/dt/WindowsContextMenu?style=flat-square)](https://packagecontrol.io/packages/WindowsContextMenu)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/jfcherng-sublime/ST-WindowsContextMenu?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-WindowsContextMenu/tags)
[![Project license](https://img.shields.io/github/license/jfcherng-sublime/ST-WindowsContextMenu?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-WindowsContextMenu/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/jfcherng-sublime/ST-WindowsContextMenu?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-WindowsContextMenu/stargazers)
[![Donate to this project using Paypal](https://img.shields.io/badge/paypal-donate-blue.svg?style=flat-square&logo=paypal)](https://www.paypal.me/jfcherng/5usd)

This is a Sublime Text plugin which adds/removes "classic" Windows context menu for Sublime Text/Merge.

![screenshot](https://raw.githubusercontent.com/jfcherng-sublime/ST-WindowsContextMenu/main/docs/screenshot.png)

## Installation

This package is available on [Package Control][package-control] by the name of [WindowsContextMenu][windowscontextmenu].

## Usage

Go to Sublime Text's main menu » `Preferences` » `Windows Context Menu`.

- Sublime Text

  - All context menus
  - Context menu for file
  - Context menu for directory
  - Context menu for directory background

- Sublime Merge

  - All context menus
  - Context menu for directory
  - Context menu for directory background

## Settings

```js
{
    // Customize the menu text in your localization.
    // If you change this, the text in existing menus will be updated immediately.
    "menu_text": "Open with {app.name}",
}
```

[windowscontextmenu]: https://packagecontrol.io/packages/WindowsContextMenu
[package-control]: https://packagecontrol.io
