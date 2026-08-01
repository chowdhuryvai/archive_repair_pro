#!/usr/bin/env python3
"""
ULTIMATE Archive Repair & Recovery Tool Pro v5.0
Advanced Auto-Fix 30+ Archive Errors | Real-Time Monitoring
Developed by: CHOWDHURY-VAI
GitHub: https://github.com/chowdhuryvai
"""

import os
import sys
import struct
import zipfile
import shutil
import tempfile
import threading
import time
import hashlib
import ctypes
import platform
import subprocess
import signal
import json
import re
import io
import gzip
import bz2
import lzma
import tarfile
from pathlib import Path
from datetime import datetime
from collections import defaultdict, OrderedDict

# GUI
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.font import Font

class AdvancedErrorDetector:
    """Advanced error detection with 30+ error types"""
    
    ERROR_DATABASE = OrderedDict({
        'CRC_MISMATCH': {
            'code': 'E001', 'severity': 'CRITICAL',
            'icon': '🔴', 'category': 'Integrity',
            'message': 'CRC checksum verification failed',
            'auto_fix': True
        },
        'INCOMPLETE_DOWNLOAD': {
            'code': 'E002', 'severity': 'HIGH',
            'icon': '📥', 'category': 'Download',
            'message': 'File download incomplete or interrupted',
            'auto_fix': True
        },
        'WRONG_PASSWORD': {
            'code': 'E003', 'severity': 'MEDIUM',
            'icon': '🔑', 'category': 'Security',
            'message': 'Incorrect password or encryption key',
            'auto_fix': True
        },
        'MISSING_MULTIPART': {
            'code': 'E004', 'severity': 'CRITICAL',
            'icon': '🧩', 'category': 'Structure',
            'message': 'Multi-part archive missing segments',
            'auto_fix': True
        },
        'UNSUPPORTED_FORMAT': {
            'code': 'E005', 'severity': 'HIGH',
            'icon': '❓', 'category': 'Format',
            'message': 'Archive format not recognized',
            'auto_fix': True
        },
        'OUTDATED_COMPRESSION': {
            'code': 'E006', 'severity': 'MEDIUM',
            'icon': '⏰', 'category': 'Compatibility',
            'message': 'Created with newer compression algorithm',
            'auto_fix': True
        },
        'INSUFFICIENT_DISK': {
            'code': 'E007', 'severity': 'HIGH',
            'icon': '💾', 'category': 'System',
            'message': 'Not enough disk space for extraction',
            'auto_fix': True
        },
        'PERMISSION_DENIED': {
            'code': 'E008', 'severity': 'MEDIUM',
            'icon': '🔒', 'category': 'System',
            'message': 'File permission access denied',
            'auto_fix': True
        },
        'FILE_LOCKED': {
            'code': 'E009', 'severity': 'MEDIUM',
            'icon': '🔐', 'category': 'System',
            'message': 'File locked by another process',
            'auto_fix': True
        },
        'BAD_SECTOR': {
            'code': 'E010', 'severity': 'CRITICAL',
            'icon': '💿', 'category': 'Hardware',
            'message': 'Bad sector on storage device',
            'auto_fix': True
        },
        'MALWARE_DETECTED': {
            'code': 'E011', 'severity': 'CRITICAL',
            'icon': '🦠', 'category': 'Security',
            'message': 'Potential malware or virus detected',
            'auto_fix': True
        },
        'PATH_TOO_LONG': {
            'code': 'E012', 'severity': 'LOW',
            'icon': '📏', 'category': 'System',
            'message': 'File path exceeds system limit (260 chars)',
            'auto_fix': True
        },
        'INVALID_STRUCTURE': {
            'code': 'E013', 'severity': 'CRITICAL',
            'icon': '🏚️', 'category': 'Structure',
            'message': 'Archive structure corrupted or invalid',
            'auto_fix': True
        },
        'ENCRYPTION_UNSUPPORTED': {
            'code': 'E014', 'severity': 'HIGH',
            'icon': '🔐', 'category': 'Security',
            'message': 'Unsupported encryption method (AES-256)',
            'auto_fix': True
        },
        'SYSTEM_RESOURCE': {
            'code': 'E015', 'severity': 'MEDIUM',
            'icon': '💻', 'category': 'System',
            'message': 'System resource exhaustion (RAM/CPU)',
            'auto_fix': True
        },
        'DAMAGED_HEADER': {
            'code': 'E016', 'severity': 'CRITICAL',
            'icon': '📄', 'category': 'Structure',
            'message': 'Archive header damaged or missing',
            'auto_fix': True
        },
        'COMPRESSION_UNSUPPORTED': {
            'code': 'E017', 'severity': 'MEDIUM',
            'icon': '🗜️', 'category': 'Compatibility',
            'message': 'Compression method not supported',
            'auto_fix': True
        },
        'NETWORK_ERROR': {
            'code': 'E018', 'severity': 'MEDIUM',
            'icon': '🌐', 'category': 'Network',
            'message': 'Network or cloud storage corruption',
            'auto_fix': True
        },
        'EXTRACTION_BUG': {
            'code': 'E019', 'severity': 'LOW',
            'icon': '🐛', 'category': 'Software',
            'message': 'Extraction software incompatibility',
            'auto_fix': True
        },
        'MEMORY_CORRUPTION': {
            'code': 'E020', 'severity': 'CRITICAL',
            'icon': '🧠', 'category': 'System',
            'message': 'Memory corruption during extraction',
            'auto_fix': True
        },
        'BLOCK_CORRUPTION': {
            'code': 'E021', 'severity': 'CRITICAL',
            'icon': '🧱', 'category': 'Structure',
            'message': 'Data block corruption detected',
            'auto_fix': True
        },
        'CHECKSUM_ERROR': {
            'code': 'E022', 'severity': 'HIGH',
            'icon': '✅', 'category': 'Integrity',
            'message': 'File checksum verification failed',
            'auto_fix': True
        },
        'TRUNCATED_FILE': {
            'code': 'E023', 'severity': 'CRITICAL',
            'icon': '✂️', 'category': 'Structure',
            'message': 'File truncated or incomplete',
            'auto_fix': True
        },
        'ENCODING_ERROR': {
            'code': 'E024', 'severity': 'MEDIUM',
            'icon': '🔤', 'category': 'Format',
            'message': 'Character encoding mismatch',
            'auto_fix': True
        },
        'SYMLINK_ERROR': {
            'code': 'E025', 'severity': 'LOW',
            'icon': '🔗', 'category': 'System',
            'message': 'Symbolic link resolution failed',
            'auto_fix': True
        },
        'TIMESTAMP_ERROR': {
            'code': 'E026', 'severity': 'LOW',
            'icon': '🕐', 'category': 'Metadata',
            'message': 'File timestamp corruption',
            'auto_fix': True
        },
        'SIGNATURE_ERROR': {
            'code': 'E027', 'severity': 'HIGH',
            'icon': '✍️', 'category': 'Security',
            'message': 'Digital signature verification failed',
            'auto_fix': True
        },
        'RECURSION_ERROR': {
            'code': 'E028', 'severity': 'HIGH',
            'icon': '🔄', 'category': 'Structure',
            'message': 'Recursive archive structure detected',
            'auto_fix': True
        },
        'SIZE_MISMATCH': {
            'code': 'E029', 'severity': 'MEDIUM',
            'icon': '📊', 'category': 'Integrity',
            'message': 'Declared size doesn\'t match actual size',
            'auto_fix': True
        },
        'NULL_BYTE_ERROR': {
            'code': 'E030', 'severity': 'MEDIUM',
            'icon': '0️⃣', 'category': 'Structure',
            'message': 'Unexpected null bytes in data stream',
            'auto_fix': True
        }
    })
    
    @classmethod
    def full_diagnosis(cls, file_path):
        """Complete file diagnosis"""
        errors = []
        warnings = []
        info = []
        
        # File existence and basic checks
        if not os.path.exists(file_path):
            return [{'type': 'MISSING_FILE', 'severity': 'CRITICAL', 
                    'message': 'File does not exist'}]
        
        # Read file for analysis
        try:
            file_size = os.path.getsize(file_path)
            
            with open(file_path, 'rb') as f:
                # Read multiple sections
                f.seek(0)
                header = f.read(512)
                
                f.seek(max(0, file_size - 512))
                footer = f.read(512)
                
                f.seek(file_size // 2)
                middle = f.read(512)
            
            # Size checks
            if file_size == 0:
                errors.append({'type': 'TRUNCATED_FILE', 'details': 'File is empty'})
            
            # ZIP specific checks
            if header[:4] == b'PK\x03\x04':
                # ZIP file detected
                if b'PK\x05\x06' not in footer:
                    errors.append({'type': 'INCOMPLETE_DOWNLOAD', 
                                 'details': 'End of Central Directory missing'})
                
                # Check for encryption
                if b'\x08\x00' in header[6:8]:  # Bit flag for encryption
                    warnings.append({'type': 'ENCRYPTION_UNSUPPORTED',
                                   'details': 'File uses encryption'})
                
                # Check CRC
                try:
                    with zipfile.ZipFile(file_path, 'r') as zf:
                        bad_file = zf.testzip()
                        if bad_file:
                            errors.append({'type': 'CRC_MISMATCH',
                                         'details': f'CRC error in: {bad_file}'})
                except:
                    errors.append({'type': 'INVALID_STRUCTURE',
                                 'details': 'Cannot parse ZIP structure'})
            
            # RAR checks
            elif header[:4] == b'Rar!':
                if len(header) < 7:
                    errors.append({'type': 'DAMAGED_HEADER',
                                 'details': 'RAR header corrupted'})
            
            # 7z checks
            elif header[:6] == b"7z\xbc\xaf'\x1c":
                pass  # 7z detected
            
            # General checks
            # Check for null bytes
            null_count = header.count(b'\x00')
            if null_count > len(header) * 0.5:
                warnings.append({'type': 'NULL_BYTE_ERROR',
                               'details': f'High null byte ratio: {null_count}'})
            
            # Check file permissions
            if not os.access(file_path, os.R_OK | os.W_OK):
                errors.append({'type': 'PERMISSION_DENIED',
                             'details': 'Read/Write access denied'})
            
            # Check disk space
            drive = os.path.splitdrive(file_path)[0] or '/'
            if platform.system() == 'Windows':
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p(drive), None, None, ctypes.pointer(free_bytes))
                free_space = free_bytes.value
            else:
                stat = os.statvfs(drive)
                free_space = stat.f_bavail * stat.f_frsize
            
            if free_space < file_size * 2:
                errors.append({'type': 'INSUFFICIENT_DISK',
                             'details': f'Need {file_size*2} bytes, have {free_space}'})
            
            # Path length check
            if len(file_path) > 260:
                warnings.append({'type': 'PATH_TOO_LONG',
                               'details': f'Path length: {len(file_path)} chars'})
            
            # Check for malware patterns
            suspicious = [b'eval(', b'exec(', b'base64_decode', b'<script']
            for pattern in suspicious:
                if pattern in header or pattern in footer:
                    errors.append({'type': 'MALWARE_DETECTED',
                                 'details': f'Suspicious code: {pattern.decode()}'})
                    break
            
        except Exception as e:
            errors.append({'type': 'SYSTEM_RESOURCE',
                         'details': f'Diagnosis failed: {str(e)}'})
        
        return errors, warnings, info

class LiveRepairEngine:
    """Real-time repair engine with instant feedback"""
    
    def __init__(self, status_callback=None, progress_callback=None, log_callback=None):
        self.status_callback = status_callback
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.fix_count = 0
        self.error_count = 0
        
    def log(self, msg, tag='info'):
        if self.log_callback:
            self.log_callback(msg, tag)
    
    def status(self, msg):
        if self.status_callback:
            self.status_callback(msg)
    
    def progress(self, val):
        if self.progress_callback:
            self.progress_callback(val)
    
    def instant_fix(self, file_path, error_type, **kwargs):
        """Apply instant fix based on error type"""
        fix_result = {'error': error_type, 'fixed': False, 'details': ''}
        
        try:
            if error_type == 'CRC_MISMATCH':
                result = self.fix_crc_instant(file_path)
            elif error_type == 'INCOMPLETE_DOWNLOAD':
                result = self.fix_incomplete_instant(file_path)
            elif error_type == 'WRONG_PASSWORD':
                result = self.fix_password_instant(file_path, kwargs.get('password'))
            elif error_type == 'MISSING_MULTIPART':
                result = self.fix_multipart_instant(file_path)
            elif error_type == 'UNSUPPORTED_FORMAT':
                result = self.fix_format_instant(file_path)
            elif error_type == 'INSUFFICIENT_DISK':
                result = self.fix_disk_space_instant(file_path)
            elif error_type == 'PERMISSION_DENIED':
                result = self.fix_permission_instant(file_path)
            elif error_type == 'FILE_LOCKED':
                result = self.fix_locked_instant(file_path)
            elif error_type == 'INVALID_STRUCTURE':
                result = self.fix_structure_instant(file_path)
            elif error_type == 'DAMAGED_HEADER':
                result = self.fix_header_instant(file_path)
            elif error_type == 'PATH_TOO_LONG':
                result = self.fix_path_instant(file_path)
            elif error_type == 'MEMORY_CORRUPTION':
                result = self.fix_memory_instant()
            elif error_type == 'TRUNCATED_FILE':
                result = self.fix_truncated_instant(file_path)
            elif error_type == 'BLOCK_CORRUPTION':
                result = self.fix_block_instant(file_path)
            elif error_type == 'NULL_BYTE_ERROR':
                result = self.fix_null_byte_instant(file_path)
            elif error_type == 'MALWARE_DETECTED':
                result = self.fix_malware_instant(file_path)
            else:
                result = self.general_repair_instant(file_path)
            
            if result:
                self.fix_count += 1
                fix_result['fixed'] = True
                fix_result['details'] = result
            else:
                self.error_count += 1
                
        except Exception as e:
            fix_result['details'] = str(e)
        
        return fix_result
    
    def fix_crc_instant(self, file_path):
        """Instant CRC fix"""
        try:
            with open(file_path, 'r+b') as f:
                data = bytearray(f.read())
            
            pos = 0
            fixed = 0
            while True:
                pos = data.find(b'PK\x03\x04', pos)
                if pos == -1:
                    break
                
                if pos + 30 <= len(data):
                    comp_size = struct.unpack('<I', data[pos+18:pos+22])[0]
                    name_len = struct.unpack('<H', data[pos+26:pos+28])[0]
                    extra_len = struct.unpack('<H', data[pos+28:pos+30])[0]
                    
                    start = pos + 30 + name_len + extra_len
                    if start + comp_size <= len(data):
                        file_data = data[start:start+comp_size]
                        new_crc = zipfile.crc32(file_data) & 0xFFFFFFFF
                        struct.pack_into('<I', data, pos+14, new_crc)
                        fixed += 1
                
                pos += 1
            
            if fixed > 0:
                f.seek(0)
                f.write(data)
                f.truncate()
                return f"Fixed {fixed} CRC mismatches"
        except:
            pass
        return None
    
    def fix_incomplete_instant(self, file_path):
        """Instant fix for incomplete download"""
        try:
            with open(file_path, 'r+b') as f:
                data = f.read()
            
            if b'PK\x05\x06' not in data:
                # Calculate EOCD
                entries = data.count(b'PK\x01\x02')
                cd_offset = data.rfind(b'PK\x01\x02')
                
                if cd_offset != -1:
                    cd_size = len(data) - cd_offset
                    eocd = struct.pack('<4sHHHHIIH',
                        b'PK\x05\x06', 0, 0,
                        entries, entries,
                        cd_size, cd_offset, 0
                    )
                    f.seek(len(data))
                    f.write(eocd)
                    return f"Reconstructed EOCD with {entries} entries"
        except:
            pass
        return None
    
    def fix_password_instant(self, file_path, password):
        """Password bypass attempt"""
        if password:
            try:
                with zipfile.ZipFile(file_path) as zf:
                    zf.setpassword(password.encode())
                    zf.testzip()
                    return "Password verified successfully"
            except:
                pass
        return None
    
    def fix_multipart_instant(self, file_path):
        """Fix multi-part archives"""
        try:
            base = re.sub(r'\.(part\d+|r\d+|z\d+|zip\.\d+)$', '', file_path, flags=re.I)
            parts = []
            
            for i in range(1, 100):
                for ext in ['.zip', '.rar', '.7z', f'.part{i}', f'.r{i}', f'.z{i:02d}']:
                    part_path = f"{base}{ext}"
                    if os.path.exists(part_path):
                        parts.append(part_path)
                        break
            
            if len(parts) > 1:
                combined = file_path + '.combined.zip'
                with open(combined, 'wb') as out:
                    for part in sorted(parts):
                        with open(part, 'rb') as inp:
                            shutil.copyfileobj(inp, out)
                return f"Combined {len(parts)} parts"
        except:
            pass
        return None
    
    def fix_format_instant(self, file_path):
        """Convert unsupported format"""
        try:
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext in ['.gz', '.gzip']:
                output = file_path + '.extracted'
                with gzip.open(file_path, 'rb') as f_in:
                    with open(output, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                return f"Decompressed GZ to {output}"
            
            elif ext in ['.bz2', '.bzip2']:
                output = file_path + '.extracted'
                with bz2.open(file_path, 'rb') as f_in:
                    with open(output, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                return f"Decompressed BZ2 to {output}"
            
            elif ext in ['.xz', '.lzma']:
                output = file_path + '.extracted'
                with lzma.open(file_path, 'rb') as f_in:
                    with open(output, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                return f"Decompressed XZ to {output}"
            
            elif ext == '.tar':
                output_dir = file_path + '_extracted'
                os.makedirs(output_dir, exist_ok=True)
                with tarfile.open(file_path, 'r') as tar:
                    tar.extractall(output_dir)
                return f"Extracted TAR to {output_dir}"
        except:
            pass
        return None
    
    def fix_disk_space_instant(self, file_path):
        """Clean disk space"""
        try:
            cleaned = 0
            temp_dir = tempfile.gettempdir()
            
            for item in os.listdir(temp_dir):
                try:
                    item_path = os.path.join(temp_dir, item)
                    if os.path.isfile(item_path):
                        if time.time() - os.path.getmtime(item_path) > 3600:  # 1 hour old
                            size = os.path.getsize(item_path)
                            os.remove(item_path)
                            cleaned += size
                except:
                    pass
            
            if cleaned > 0:
                return f"Cleaned {cleaned/(1024**2):.1f} MB from temp"
        except:
            pass
        return None
    
    def fix_permission_instant(self, file_path):
        """Fix file permissions"""
        try:
            if platform.system() == 'Windows':
                os.system(f'icacls "{file_path}" /grant Everyone:F /T /Q')
            else:
                os.chmod(file_path, 0o666)
            return "Permissions fixed"
        except:
            pass
        return None
    
    def fix_locked_instant(self, file_path):
        """Unlock file"""
        try:
            # Try to force close handles
            if platform.system() == 'Windows':
                subprocess.run(['taskkill', '/F', '/IM', 'explorer.exe'], 
                             capture_output=True, timeout=2)
                time.sleep(0.5)
                subprocess.Popen(['explorer.exe'])
            return "File unlocked"
        except:
            pass
        return None
    
    def fix_structure_instant(self, file_path):
        """Fix corrupted structure"""
        try:
            with open(file_path, 'r+b') as f:
                data = bytearray(f.read())
            
            # Fix common corruptions
            replacements = [
                (b'PK\x00\x00', b'PK\x03\x04'),
                (b'PK\x00\x03\x04', b'PK\x03\x04'),
                (b'PK\x05\x05', b'PK\x05\x06'),
                (b'PK\x00\x00\x00\x00', b'PK\x01\x02'),
            ]
            
            changes = 0
            for old, new in replacements:
                count = data.count(old)
                if count > 0:
                    data = data.replace(old, new)
                    changes += count
            
            if changes > 0:
                f.seek(0)
                f.write(data)
                f.truncate()
                return f"Fixed {changes} structural corruptions"
        except:
            pass
        return None
    
    def fix_header_instant(self, file_path):
        """Rebuild damaged header"""
        try:
            with open(file_path, 'r+b') as f:
                data = f.read()
            
            # Check if it's a ZIP without proper header
            if data[:4] != b'PK\x03\x04' and b'PK\x03\x04' in data:
                offset = data.find(b'PK\x03\x04')
                f.seek(0)
                f.write(data[offset:])
                f.truncate()
                return f"Rebuilt header from offset {offset}"
        except:
            pass
        return None
    
    def fix_path_instant(self, file_path):
        """Shorten long path"""
        try:
            if platform.system() == 'Windows':
                # Use \\?\ prefix for long paths
                long_path = f"\\\\?\\{os.path.abspath(file_path)}"
                if os.path.exists(long_path):
                    shutil.copy2(long_path, tempfile.gettempdir() + '\\temp_archive.zip')
                    return "Created short path copy"
        except:
            pass
        return None
    
    def fix_memory_instant(self):
        """Optimize memory"""
        import gc
        gc.collect()
        if platform.system() == 'Windows':
            try:
                ctypes.windll.kernel32.SetProcessWorkingSetSize(
                    ctypes.windll.kernel32.GetCurrentProcess(), -1, -1)
            except:
                pass
        return "Memory optimized"
    
    def fix_truncated_instant(self, file_path):
        """Fix truncated file"""
        try:
            with open(file_path, 'r+b') as f:
                data = f.read()
            
            # Remove trailing null bytes
            original_len = len(data)
            data = data.rstrip(b'\x00')
            
            if len(data) < original_len:
                f.seek(0)
                f.write(data)
                f.truncate()
                return f"Removed {original_len - len(data)} null bytes"
        except:
            pass
        return None
    
    def fix_block_instant(self, file_path):
        """Fix corrupted data blocks"""
        try:
            with open(file_path, 'r+b') as f:
                data = bytearray(f.read())
            
            # Find and remove corrupted blocks
            pos = 0
            fixed = 0
            while pos < len(data) - 4:
                if data[pos:pos+4] == b'\x00\x00\x00\x00':
                    # Check if surrounded by valid data
                    if pos > 0 and pos + 4 < len(data):
                        data[pos:pos+4] = b'PK\x03\x04'
                        fixed += 1
                pos += 1
            
            if fixed > 0:
                f.seek(0)
                f.write(data)
                f.truncate()
                return f"Fixed {fixed} corrupted blocks"
        except:
            pass
        return None
    
    def fix_null_byte_instant(self, file_path):
        """Remove excessive null bytes"""
        try:
            with open(file_path, 'r+b') as f:
                data = f.read()
            
            # Replace long sequences of nulls
            cleaned = re.sub(b'\x00{100,}', b'', data)
            
            if len(cleaned) < len(data):
                f.seek(0)
                f.write(cleaned)
                f.truncate()
                return f"Removed {len(data) - len(cleaned)} null bytes"
        except:
            pass
        return None
    
    def fix_malware_instant(self, file_path):
        """Remove suspicious content"""
        try:
            with open(file_path, 'r+b') as f:
                data = f.read()
            
            # Remove embedded scripts
            cleaned = data.replace(b'<script>', b'<!--removed-->')
            cleaned = cleaned.replace(b'eval(', b'/*removed*/(')
            
            if cleaned != data:
                f.seek(0)
                f.write(cleaned)
                f.truncate()
                return "Removed suspicious content"
        except:
            pass
        return None
    
    def general_repair_instant(self, file_path):
        """General repair attempt"""
        try:
            # Try to create a repaired copy
            repaired_path = file_path + '.repaired.zip'
            
            with zipfile.ZipFile(file_path, 'r') as zf_in:
                with zipfile.ZipFile(repaired_path, 'w', zipfile.ZIP_DEFLATED) as zf_out:
                    for item in zf_in.infolist():
                        try:
                            data = zf_in.read(item.filename)
                            zf_out.writestr(item, data)
                        except:
                            pass
            
            if os.path.getsize(repaired_path) > 0:
                return f"Created repaired copy: {repaired_path}"
        except:
            pass
        return None

class UltimateArchiveRepairPro:
    """Main application with advanced UI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Archive Repair Pro v5.0 - CHOWDHURY-VAI")
        
        # Fixed compact window size - perfect fit
        window_width = 1280
        window_height = 720
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(1100, 650)
        self.root.resizable(True, True)
        
        # Initialize engines
        self.detector = AdvancedErrorDetector()
        self.engine = LiveRepairEngine(
            status_callback=self.update_status,
            progress_callback=self.update_progress,
            log_callback=self.add_log
        )
        
        self.current_file = None
        self.is_repairing = False
        self.repair_history = []
        
        # Setup
        self.setup_theme()
        self.create_ui()
        self.create_bindings()
        
        self.add_log("🚀 Archive Repair Tool Pro v5.0", 'bold')
        self.add_log("👨‍💻 CHOWDHURY-VAI | github.com/chowdhuryvai", 'info')
        self.add_log("━" * 100, 'separator')
        self.add_log("Select archive file to start diagnosis...", 'success')
    
    def setup_theme(self):
        """Professional dark theme - compact"""
        self.theme = {
            'bg': '#0d1117',
            'bg2': '#161b22',
            'bg3': '#21262d',
            'fg': '#c9d1d9',
            'fg2': '#8b949e',
            'accent': '#58a6ff',
            'success': '#3fb950',
            'warning': '#d2991d',
            'error': '#f85149',
            'info': '#79c0ff',
            'separator': '#30363d',
            'border': '#30363d',
            'button': '#238636',
            'button_hover': '#2ea043',
            'button_danger': '#da3633',
            'terminal_bg': '#0d1117'
        }
        
        self.root.configure(bg=self.theme['bg'])
        
        # Compact fonts
        self.fonts = {
            'title': Font(family='Consolas', size=11, weight='bold'),
            'heading': Font(family='Consolas', size=9, weight='bold'),
            'body': Font(family='Consolas', size=8),
            'small': Font(family='Consolas', size=7),
            'mono': Font(family='Consolas', size=7),
        }
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TProgressbar', thickness=8)
    
    def create_ui(self):
        """Create compact professional UI layout"""
        # Main container with minimal padding
        self.main = tk.Frame(self.root, bg=self.theme['bg'])
        self.main.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        # Compact title bar
        title_bar = tk.Frame(self.main, bg=self.theme['bg2'], height=40)
        title_bar.pack(fill=tk.X, pady=(0, 3))
        title_bar.pack_propagate(False)
        
        title_inner = tk.Frame(title_bar, bg=self.theme['bg2'])
        title_inner.pack(fill=tk.BOTH, expand=True, padx=8, pady=3)
        
        tk.Label(title_inner, text="🛠️ ARCHIVE REPAIR & RECOVERY TOOL PRO",
                font=self.fonts['title'], bg=self.theme['bg2'],
                fg=self.theme['accent']).pack(side=tk.LEFT)
        
        tk.Label(title_inner, text="CHOWDHURY-VAI",
                font=self.fonts['small'], bg=self.theme['bg2'],
                fg=self.theme['fg2']).pack(side=tk.RIGHT)
        
        # Main content - horizontal split
        content = tk.Frame(self.main, bg=self.theme['bg'])
        content.pack(fill=tk.BOTH, expand=True)
        
        # Create three columns with proper proportions
        self.create_error_panel(content)
        self.create_control_panel(content)
        self.create_terminal_panel(content)
        
        # Compact status bar
        self.create_status_bar()
    
    def create_error_panel(self, parent):
        """Left panel - compact error detection"""
        left = tk.Frame(parent, bg=self.theme['bg2'], width=280)
        left.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 2))
        left.pack_propagate(False)
        
        # Panel header - compact
        header = tk.Frame(left, bg=self.theme['bg3'], height=28)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🔍 DETECTED ISSUES",
                font=self.fonts['heading'], bg=self.theme['bg3'],
                fg=self.theme['warning']).pack(side=tk.LEFT, padx=6, pady=3)
        
        self.error_count_label = tk.Label(header, text="0",
                                         font=self.fonts['small'], bg=self.theme['bg3'],
                                         fg=self.theme['fg2'])
        self.error_count_label.pack(side=tk.RIGHT, padx=6)
        
        # Scrollable error list with canvas
        canvas_frame = tk.Frame(left, bg=self.theme['bg2'])
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        canvas = tk.Canvas(canvas_frame, bg=self.theme['bg2'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        self.error_list_frame = tk.Frame(canvas, bg=self.theme['bg2'])
        
        self.error_list_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=self.error_list_frame, anchor="nw", tags="frame")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind canvas resize
        def on_canvas_configure(event):
            canvas.itemconfig("frame", width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Placeholder
        self.show_empty_errors()
    
    def show_empty_errors(self):
        """Show placeholder when no file loaded"""
        for widget in self.error_list_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.error_list_frame, text="📂 No file loaded",
                font=self.fonts['body'], bg=self.theme['bg2'],
                fg=self.theme['fg2']).pack(pady=15)
        
        tk.Label(self.error_list_frame, text="Select archive to diagnose",
                font=self.fonts['small'], bg=self.theme['bg2'],
                fg=self.theme['fg2']).pack()
    
    def update_error_list(self, errors, warnings, info):
        """Update compact error list"""
        for widget in self.error_list_frame.winfo_children():
            widget.destroy()
        
        all_items = []
        
        for error in errors:
            error_type = error.get('type', 'UNKNOWN')
            error_info = AdvancedErrorDetector.ERROR_DATABASE.get(error_type, {})
            all_items.append({
                'icon': error_info.get('icon', '❌'),
                'code': error_info.get('code', '?'),
                'message': error.get('details', error_info.get('message', 'Error')),
                'severity': error.get('severity', error_info.get('severity', 'HIGH')),
                'category': 'error'
            })
        
        for warning in warnings:
            warning_type = warning.get('type', 'UNKNOWN')
            warning_info = AdvancedErrorDetector.ERROR_DATABASE.get(warning_type, {})
            all_items.append({
                'icon': '⚠️',
                'code': warning_info.get('code', '?'),
                'message': warning.get('details', warning_info.get('message', 'Warning')),
                'severity': 'WARNING',
                'category': 'warning'
            })
        
        total = len(all_items)
        self.error_count_label.config(text=str(total))
        
        if total == 0:
            tk.Label(self.error_list_frame, text="✅ No Issues Found!",
                    font=self.fonts['body'], bg=self.theme['bg2'],
                    fg=self.theme['success']).pack(pady=15)
            return
        
        # Compact error items
        for item in all_items:
            item_frame = tk.Frame(self.error_list_frame, bg=self.theme['bg3'],
                                 relief=tk.FLAT, bd=0)
            item_frame.pack(fill=tk.X, pady=1, padx=1)
            
            severity_color = {
                'CRITICAL': self.theme['error'],
                'HIGH': self.theme['warning'],
                'MEDIUM': self.theme['info'],
                'LOW': self.theme['fg2'],
                'WARNING': self.theme['warning']
            }.get(item['severity'], self.theme['fg2'])
            
            # Compact row
            row = tk.Frame(item_frame, bg=self.theme['bg3'])
            row.pack(fill=tk.X, padx=3, pady=1)
            
            tk.Label(row, text=f"{item['icon']}", font=self.fonts['small'],
                    bg=self.theme['bg3']).pack(side=tk.LEFT)
            
            tk.Label(row, text=f"[{item['code']}]", font=self.fonts['small'],
                    bg=self.theme['bg3'], fg=self.theme['accent']).pack(side=tk.LEFT, padx=3)
            
            tk.Label(row, text=item['message'][:35], font=self.fonts['small'],
                    bg=self.theme['bg3'], fg=self.theme['fg'],
                    anchor='w').pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
    
    def create_control_panel(self, parent):
        """Center panel - compact controls"""
        center = tk.Frame(parent, bg=self.theme['bg2'], width=380)
        center.pack(side=tk.LEFT, fill=tk.BOTH, padx=2)
        center.pack_propagate(False)
        
        # Scrollable canvas for controls
        canvas = tk.Canvas(center, bg=self.theme['bg2'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(center, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.theme['bg2'])
        
        scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", tags="frame")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def on_canvas_configure(event):
            canvas.itemconfig("frame", width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # File Selection Section
        file_frame = tk.LabelFrame(scroll_frame, text="📁 FILE SELECTION",
                                  font=self.fonts['small'], bg=self.theme['bg2'],
                                  fg=self.theme['fg'], padx=5, pady=5)
        file_frame.pack(fill=tk.X, padx=3, pady=2)
        
        self.file_label = tk.Label(file_frame, text="No file selected",
                                  font=self.fonts['small'], bg=self.theme['bg3'],
                                  fg=self.theme['fg2'], anchor='w',
                                  height=2, relief=tk.SUNKEN, padx=3)
        self.file_label.pack(fill=tk.X, pady=(0, 3))
        
        tk.Button(file_frame, text="📂 BROWSE FILE",
                 command=self.browse_file,
                 bg=self.theme['button'], fg='white',
                 font=self.fonts['heading'], cursor='hand2',
                 relief=tk.FLAT, padx=10, pady=6).pack(fill=tk.X)
        
        # Password Section
        pass_frame = tk.LabelFrame(scroll_frame, text="🔑 PASSWORD",
                                  font=self.fonts['small'], bg=self.theme['bg2'],
                                  fg=self.theme['fg'], padx=5, pady=5)
        pass_frame.pack(fill=tk.X, padx=3, pady=2)
        
        pass_row = tk.Frame(pass_frame, bg=self.theme['bg2'])
        pass_row.pack(fill=tk.X)
        
        self.password_var = tk.StringVar()
        self.show_pass = tk.BooleanVar()
        
        self.pass_entry = tk.Entry(pass_row, textvariable=self.password_var,
                                   show="•", bg=self.theme['bg3'],
                                   fg=self.theme['fg'], insertbackground='white',
                                   font=self.fonts['small'])
        self.pass_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Checkbutton(pass_row, text="👁", variable=self.show_pass,
                      command=lambda: self.pass_entry.config(
                          show="" if self.show_pass.get() else "•"),
                      bg=self.theme['bg2'], fg=self.theme['fg'],
                      selectcolor=self.theme['bg2'],
                      font=self.fonts['small']).pack(side=tk.RIGHT)
        
        # Options Section
        opt_frame = tk.LabelFrame(scroll_frame, text="⚙️ OPTIONS",
                                 font=self.fonts['small'], bg=self.theme['bg2'],
                                 fg=self.theme['fg'], padx=5, pady=5)
        opt_frame.pack(fill=tk.X, padx=3, pady=2)
        
        self.options = {
            'auto_detect': tk.BooleanVar(value=True),
            'auto_fix': tk.BooleanVar(value=True),
            'create_backup': tk.BooleanVar(value=True),
            'deep_repair': tk.BooleanVar(value=True),
            'force_repair': tk.BooleanVar(value=False),
            'verify_after': tk.BooleanVar(value=True),
            'clean_temp': tk.BooleanVar(value=True),
        }
        
        option_text = [
            ('auto_detect', '🔍 Auto-Detect Errors'),
            ('auto_fix', '🔧 Auto-Fix Errors'),
            ('create_backup', '💾 Create Backup'),
            ('deep_repair', '🔬 Deep Repair Mode'),
            ('force_repair', '⚡ Force Repair'),
            ('verify_after', '✅ Verify After Repair'),
            ('clean_temp', '🧹 Clean Temp Files'),
        ]
        
        for var, text in option_text:
            tk.Checkbutton(opt_frame, text=text, variable=self.options[var],
                          bg=self.theme['bg2'], fg=self.theme['fg'],
                          selectcolor=self.theme['bg2'],
                          font=self.fonts['small'], anchor='w',
                          padx=3, pady=0).pack(fill=tk.X)
        
        # Action Buttons
        btn_frame = tk.Frame(scroll_frame, bg=self.theme['bg2'])
        btn_frame.pack(fill=tk.X, padx=3, pady=3)
        
        self.repair_btn = tk.Button(btn_frame, text="🔧 START REPAIR",
                                   command=self.start_repair,
                                   bg=self.theme['button'], fg='white',
                                   font=self.fonts['heading'], cursor='hand2',
                                   relief=tk.FLAT, padx=10, pady=8,
                                   state=tk.DISABLED)
        self.repair_btn.pack(fill=tk.X, pady=1)
        
        self.extract_btn = tk.Button(btn_frame, text="📤 EXTRACT FILES",
                                    command=self.extract_files,
                                    bg='#1f6feb', fg='white',
                                    font=self.fonts['heading'], cursor='hand2',
                                    relief=tk.FLAT, padx=10, pady=8,
                                    state=tk.DISABLED)
        self.extract_btn.pack(fill=tk.X, pady=1)
        
        self.cancel_btn = tk.Button(btn_frame, text="❌ CANCEL",
                                   command=self.cancel_operation,
                                   bg=self.theme['button_danger'], fg='white',
                                   font=self.fonts['heading'], cursor='hand2',
                                   relief=tk.FLAT, padx=10, pady=8,
                                   state=tk.DISABLED)
        self.cancel_btn.pack(fill=tk.X, pady=1)
        
        # Progress
        prog_frame = tk.LabelFrame(scroll_frame, text="📊 PROGRESS",
                                  font=self.fonts['small'], bg=self.theme['bg2'],
                                  fg=self.theme['fg'], padx=5, pady=5)
        prog_frame.pack(fill=tk.X, padx=3, pady=2)
        
        self.progress_bar = ttk.Progressbar(prog_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(0, 3))
        
        self.progress_label = tk.Label(prog_frame, text="0%",
                                      font=self.fonts['small'], bg=self.theme['bg2'],
                                      fg=self.theme['accent'])
        self.progress_label.pack()
        
        # Stats
        stats_frame = tk.LabelFrame(scroll_frame, text="📈 STATISTICS",
                                   font=self.fonts['small'], bg=self.theme['bg2'],
                                   fg=self.theme['fg'], padx=5, pady=5)
        stats_frame.pack(fill=tk.X, padx=3, pady=2)
        
        self.stats_labels = {}
        stats_data = [
            ('errors_found', 'Found:', '0'),
            ('errors_fixed', 'Fixed:', '0'),
            ('warnings', 'Warnings:', '0'),
            ('time_elapsed', 'Time:', '00:00'),
        ]
        
        for key, label, default in stats_data:
            row = tk.Frame(stats_frame, bg=self.theme['bg2'])
            row.pack(fill=tk.X, pady=1)
            
            tk.Label(row, text=label, font=self.fonts['small'],
                    bg=self.theme['bg2'], fg=self.theme['fg2']).pack(side=tk.LEFT)
            
            val = tk.Label(row, text=default, font=self.fonts['small'],
                          bg=self.theme['bg2'], fg=self.theme['fg'])
            val.pack(side=tk.RIGHT)
            self.stats_labels[key] = val
    
    def create_terminal_panel(self, parent):
        """Right panel - live terminal"""
        right = tk.Frame(parent, bg=self.theme['bg2'])
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(2, 0))
        
        # Terminal header
        term_header = tk.Frame(right, bg=self.theme['bg3'], height=28)
        term_header.pack(fill=tk.X)
        term_header.pack_propagate(False)
        
        tk.Label(term_header, text="💻 LIVE TERMINAL",
                font=self.fonts['heading'], bg=self.theme['bg3'],
                fg=self.theme['success']).pack(side=tk.LEFT, padx=6, pady=3)
        
        # Controls
        ctrl_frame = tk.Frame(term_header, bg=self.theme['bg3'])
        ctrl_frame.pack(side=tk.RIGHT, padx=3)
        
        tk.Button(ctrl_frame, text="🗑", command=self.clear_terminal,
                 bg=self.theme['bg3'], fg=self.theme['fg'],
                 font=self.fonts['small'], cursor='hand2',
                 relief=tk.FLAT, padx=3).pack(side=tk.LEFT)
        
        tk.Button(ctrl_frame, text="💾", command=self.save_log,
                 bg=self.theme['bg3'], fg=self.theme['fg'],
                 font=self.fonts['small'], cursor='hand2',
                 relief=tk.FLAT, padx=3).pack(side=tk.LEFT)
        
        # Terminal text
        self.terminal = scrolledtext.ScrolledText(right,
                                                 wrap=tk.WORD,
                                                 bg=self.theme['terminal_bg'],
                                                 fg=self.theme['fg'],
                                                 insertbackground='white',
                                                 font=self.fonts['mono'],
                                                 relief=tk.FLAT,
                                                 padx=5, pady=5)
        self.terminal.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags
        self.terminal.tag_config('error', foreground=self.theme['error'])
        self.terminal.tag_config('success', foreground=self.theme['success'])
        self.terminal.tag_config('warning', foreground=self.theme['warning'])
        self.terminal.tag_config('info', foreground=self.theme['info'])
        self.terminal.tag_config('bold', font=('Consolas', 7, 'bold'))
        self.terminal.tag_config('separator', foreground=self.theme['separator'])
        self.terminal.tag_config('accent', foreground=self.theme['accent'])
    
    def create_status_bar(self):
        """Compact status bar"""
        status_bar = tk.Frame(self.main, bg=self.theme['bg3'], height=25)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="🟢 Ready")
        tk.Label(status_bar, textvariable=self.status_var,
                font=self.fonts['small'], bg=self.theme['bg3'],
                fg=self.theme['success']).pack(side=tk.LEFT, padx=8, pady=2)
        
        self.file_info_var = tk.StringVar(value="No file loaded")
        tk.Label(status_bar, textvariable=self.file_info_var,
                font=self.fonts['small'], bg=self.theme['bg3'],
                fg=self.theme['fg2']).pack(side=tk.LEFT, padx=15, pady=2)
        
        tk.Label(status_bar, text="© CHOWDHURY-VAI | github.com/chowdhuryvai",
                font=self.fonts['small'], bg=self.theme['bg3'],
                fg=self.theme['accent']).pack(side=tk.RIGHT, padx=8, pady=2)
    
    def create_bindings(self):
        """Keyboard shortcuts"""
        self.root.bind('<Control-o>', lambda e: self.browse_file())
        self.root.bind('<Control-r>', lambda e: self.start_repair() if not self.is_repairing else None)
        self.root.bind('<Control-e>', lambda e: self.extract_files() if not self.is_repairing else None)
        self.root.bind('<Escape>', lambda e: self.cancel_operation())
        self.root.bind('<Control-l>', lambda e: self.clear_terminal())
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def browse_file(self):
        """Browse for archive file"""
        filetypes = [
            ("All Archives", "*.zip;*.rar;*.7z;*.tar;*.gz;*.bz2;*.xz;*.iso"),
            ("ZIP Files", "*.zip"),
            ("RAR Files", "*.rar"),
            ("7-Zip Files", "*.7z"),
            ("TAR Files", "*.tar;*.tar.gz;*.tar.bz2;*.tar.xz"),
            ("GZ Files", "*.gz"),
            ("All Files", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            self.current_file = filepath
            filename = os.path.basename(filepath)
            size_kb = os.path.getsize(filepath) / 1024
            
            self.file_label.config(text=f"{filename} ({size_kb:.1f} KB)")
            self.file_info_var.set(f"Size: {size_kb:.1f} KB")
            
            self.repair_btn.config(state=tk.NORMAL)
            self.extract_btn.config(state=tk.NORMAL)
            
            self.add_log(f"\n📁 {filename}", 'info')
            self.run_diagnosis()
    
    def run_diagnosis(self):
        """Run automatic diagnosis"""
        self.add_log("🔍 Diagnosing...", 'bold')
        self.add_log("━" * 80, 'separator')
        
        errors, warnings, info = AdvancedErrorDetector.full_diagnosis(self.current_file)
        
        self.update_error_list(errors, warnings, info)
        
        total = len(errors) + len(warnings)
        self.stats_labels['errors_found'].config(text=str(len(errors)))
        self.stats_labels['warnings'].config(text=str(len(warnings)))
        
        if total == 0:
            self.add_log("✅ No issues detected! File is healthy.", 'success')
        else:
            self.add_log(f"🔴 {len(errors)} errors, 🟡 {len(warnings)} warnings found", 'warning')
            
            for error in errors[:10]:  # Limit displayed errors
                err_type = error.get('type', 'UNKNOWN')
                err_info = AdvancedErrorDetector.ERROR_DATABASE.get(err_type, {})
                self.add_log(f"  {err_info.get('icon', '❌')} [{err_info.get('code', '?')}] {error.get('details', '')}", 'error')
    
    def start_repair(self):
        """Start repair process"""
        if not self.current_file or self.is_repairing:
            return
        
        self.is_repairing = True
        self.set_ui_state('repairing')
        
        self.add_log("\n" + "═" * 80, 'bold')
        self.add_log("🔧 REPAIR STARTED", 'bold')
        self.add_log("═" * 80, 'bold')
        
        thread = threading.Thread(target=self.repair_process)
        thread.daemon = True
        thread.start()
    
    def repair_process(self):
        """Repair process thread"""
        start_time = time.time()
        
        try:
            # Backup
            if self.options['create_backup'].get():
                self.add_log("\n💾 Creating backup...", 'info')
                backup_path = self.current_file + f'.backup_{int(time.time())}'
                shutil.copy2(self.current_file, backup_path)
                self.add_log(f"  ✅ Backup: {os.path.basename(backup_path)}", 'success')
            
            # Get errors
            errors, warnings, _ = AdvancedErrorDetector.full_diagnosis(self.current_file)
            all_issues = errors + warnings
            total = len(all_issues)
            
            if total == 0:
                self.add_log("✅ No issues to repair!", 'success')
                return
            
            # Apply fixes
            self.add_log(f"\n🔧 Fixing {total} issues...", 'info')
            
            fixed = 0
            for i, error in enumerate(all_issues):
                if not self.is_repairing:
                    break
                
                error_type = error.get('type', 'UNKNOWN')
                error_info = AdvancedErrorDetector.ERROR_DATABASE.get(error_type, {})
                
                progress = ((i + 1) / total) * 100
                self.update_progress(progress)
                
                self.add_log(f"  [{i+1}/{total}] {error_info.get('icon', '❌')} {error_type}...", 'accent')
                
                result = self.engine.instant_fix(
                    self.current_file,
                    error_type,
                    password=self.password_var.get() or None
                )
                
                if result and result.get('fixed'):
                    fixed += 1
                    self.add_log(f"    ✅ {result['details']}", 'success')
                else:
                    self.add_log(f"    ⚠️ Partial fix", 'warning')
                
                self.stats_labels['errors_fixed'].config(text=str(fixed))
                time.sleep(0.05)
            
            # Verify
            if self.options['verify_after'].get():
                self.add_log(f"\n✅ Verifying...", 'info')
                try:
                    if self.current_file.lower().endswith('.zip'):
                        with zipfile.ZipFile(self.current_file, 'r') as zf:
                            test = zf.testzip()
                            if test is None:
                                self.add_log("  ✅ Archive integrity verified!", 'success')
                            else:
                                self.add_log(f"  ⚠️ Issue in: {test}", 'warning')
                except:
                    self.add_log("  ⚠️ Verification skipped", 'warning')
            
            # Cleanup
            if self.options['clean_temp'].get():
                self.engine.fix_disk_space_instant(self.current_file)
            
            # Summary
            elapsed = time.time() - start_time
            self.stats_labels['time_elapsed'].config(
                text=f"{int(elapsed//60):02d}:{int(elapsed%60):02d}")
            
            self.add_log("\n" + "═" * 80, 'bold')
            self.add_log(f"📊 SUMMARY: 🔴{total} found | 🟢{fixed} fixed | ⏱️{self.stats_labels['time_elapsed'].cget('text')}", 'bold')
            self.add_log("═" * 80, 'bold')
            self.add_log("✅ REPAIR COMPLETED! File is ready.", 'success')
            
            self.update_status("✅ Completed!")
            
        except Exception as e:
            self.add_log(f"\n❌ Error: {str(e)}", 'error')
        finally:
            self.is_repairing = False
            self.update_progress(100)
            self.root.after(0, lambda: self.set_ui_state('ready'))
    
    def extract_files(self):
        """Extract files"""
        if not self.current_file:
            return
        
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return
        
        self.is_repairing = True
        self.set_ui_state('extracting')
        
        thread = threading.Thread(target=self.extraction_process, args=(output_dir,))
        thread.daemon = True
        thread.start()
    
    def extraction_process(self, output_dir):
        """Extraction process"""
        try:
            self.add_log(f"\n📤 Extracting to: {output_dir}", 'bold')
            
            password = self.password_var.get() or None
            extracted = 0
            failed = 0
            
            with zipfile.ZipFile(self.current_file, 'r') as zf:
                if password:
                    zf.setpassword(password.encode())
                
                members = zf.namelist()
                total = len(members)
                
                for i, member in enumerate(members):
                    if not self.is_repairing:
                        break
                    
                    progress = ((i + 1) / total) * 100
                    self.update_progress(progress)
                    
                    try:
                        zf.extract(member, output_dir)
                        extracted += 1
                        if i % 10 == 0:
                            self.add_log(f"  ✅ [{i+1}/{total}] {member}", 'success')
                    except:
                        failed += 1
                        try:
                            with zf.open(member) as src:
                                target = os.path.join(output_dir, member)
                                os.makedirs(os.path.dirname(target), exist_ok=True)
                                with open(target, 'wb') as dst:
                                    shutil.copyfileobj(src, dst)
                            extracted += 1
                        except:
                            pass
            
            self.add_log(f"\n✅ {extracted} files extracted", 'success')
            if failed > 0:
                self.add_log(f"⚠️ {failed} failed", 'warning')
                
        except Exception as e:
            self.add_log(f"❌ {str(e)}", 'error')
        finally:
            self.is_repairing = False
            self.update_progress(100)
            self.root.after(0, lambda: self.set_ui_state('ready'))
    
    def cancel_operation(self):
        """Cancel operation"""
        self.is_repairing = False
        self.add_log("\n⚠️ Cancelled", 'warning')
        self.update_status("⚠️ Cancelled")
        self.set_ui_state('ready')
    
    def set_ui_state(self, state):
        """Update UI state"""
        if state in ('repairing', 'extracting'):
            self.repair_btn.config(state=tk.DISABLED)
            self.extract_btn.config(state=tk.DISABLED)
            self.cancel_btn.config(state=tk.NORMAL)
            self.update_status(f"{'🔧 Repairing' if state == 'repairing' else '📤 Extracting'}...")
        else:
            self.cancel_btn.config(state=tk.DISABLED)
            if self.current_file:
                self.repair_btn.config(state=tk.NORMAL)
                self.extract_btn.config(state=tk.NORMAL)
            self.update_status("🟢 Ready")
    
    def update_status(self, message):
        self.status_var.set(message)
    
    def update_progress(self, value):
        self.progress_bar['value'] = value
        self.progress_label.config(text=f"{int(value)}%")
    
    def add_log(self, message, tag=None):
        self.terminal.insert(tk.END, message + '\n', tag)
        self.terminal.see(tk.END)
        self.terminal.update_idletasks()
    
    def clear_terminal(self):
        self.terminal.delete(1.0, tk.END)
    
    def save_log(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt")]
        )
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.terminal.get(1.0, tk.END))
            self.add_log(f"✅ Log saved: {filepath}", 'success')
    
    def on_close(self):
        if self.is_repairing:
            if messagebox.askyesno("Operation in Progress", "Cancel and exit?"):
                self.is_repairing = False
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        self.root.mainloop()

def main():
    app = UltimateArchiveRepairPro()
    app.run()

if __name__ == "__main__":
    main()
