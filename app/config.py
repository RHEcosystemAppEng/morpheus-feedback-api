# SPDX-FileCopyrightText: Copyright (c) 2025, Red Hat Inc. & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
# Replace these placeholders with actual credentials or set via environment variables.
class Config:
    # Configuration loaded from environment variables with defaults
    ARGILLA_API_KEY = os.environ.get('ARGILLA_API_KEY', 'admin.apikey')
    ARGILLA_API_URL = os.environ.get('ARGILLA_API_URL', 'http://localhost:6900')
    ARGILLA_DATASET = os.environ.get('ARGILLA_DATASET', 'feedback-ai')
    ARGILLA_WORKSPACE = os.environ.get('ARGILLA_WORKSPACE', 'admin')
